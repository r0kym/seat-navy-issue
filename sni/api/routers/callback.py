"""
Callback paths
"""

import logging
from typing import List, Sequence

from fastapi import APIRouter, status
from fastapi.responses import (
    HTMLResponse,
    PlainTextResponse,
    RedirectResponse,
)
import requests

from sni.user.models import User

from sni.esi.sso import (
    decode_access_token,
    EsiTokenError,
    get_access_token_from_callback_code,
)
from sni.esi.scope import EsiScope
from sni.esi.token import save_esi_tokens, token_has_enough_scopes
from sni.uac.token import create_user_token, StateCode, to_jwt
from sni.uac.uac import is_authorized_to_login

router = APIRouter()


def token_manipulation_error_response() -> HTMLResponse:
    """
    Returns an HTML response explaing that the instance ran in an ESI token
    manipulation error.
    """
    return HTMLResponse(
        content="""<h1>ESI token manipulation error</h1>
<p>Sorry, something went wrong while manipulating your ESI token. It could be a
temporary outage of the EVE API, or a bug in SeAT Navy Issue.</p>
<p>If the problem persists, please contact the instance administrator.</p>""",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def not_authorized_to_login_response(
    character_name: str, character_id: int
) -> HTMLResponse:
    """
    Returns an HTML response explaing that the user is not allowed to login on
    this instance.
    """
    return HTMLResponse(
        content=f"""<h1>Not authorized to login</h1>
<p>Character <strong>{character_name}</strong> ({character_id}) is not allowed
to login. This is due to the fact that your character and/or corporation and/or
alliance is not whitelisted.</p>
<p>If your alliance recently joined a coalition registered on this instance,
ask the coalition managed to add your alliance, and try again.</p>
<p>If the problem persists, please contact the instance administrator.</p>
""",
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


def string_list_to_html(string_list: Sequence[str]) -> str:
    """
    Converts a string list to an HTML bullet list.
    """
    if not string_list:
        return "<p>None</p>"
    item_list = [f"<li><code>{item}</code></li>" for item in string_list]
    return "<ul>" + "".join(item_list) + "</ul>"


def not_enough_scopes_response(
    character_name: str,
    character_id: int,
    required_scopes: List[EsiScope],
    provided_scopes: List[EsiScope],
) -> HTMLResponse:
    """
    Returns an HTML response explaing that the user did not provide enough ESI
    scopes.
    """
    return HTMLResponse(
        content=f"""<h1>Not enough ESI scopes</h1>
<p>The ESI token does not provide enough scopes for character
<strong>{character_name}</strong> ({character_id}):</p>
<h3>Required</h3>
{string_list_to_html(required_scopes)}
<h3>Provided</h3>
{string_list_to_html(provided_scopes)}
""",
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


@router.get(
    "/esi", summary="ESI callback",
)
async def get_callback_esi(code: str, state: str):
    """
    ESI callback. You should not manually call this.

    Upon receiving a notification from EVE SSO, SNI redirects the client to the
    appropriate frontend callback, with the state code and user token in URL
    parameters.

    Reference:
        `OAuth 2.0 for Web Based Applications <https://docs.esi.evetech.net/docs/sso/web_based_sso_flow.html>`_
    """
    logging.info("Received callback from ESI for state %s", state)

    state_code: StateCode = StateCode.objects.get(uuid=state)
    state_code.delete()

    try:
        esi_response = get_access_token_from_callback_code(code)
        access_token = decode_access_token(esi_response.access_token)
        save_esi_tokens(esi_response)
    except EsiTokenError:
        return token_manipulation_error_response()

    usr: User = User.objects.get(character_id=access_token.character_id)
    if state_code.inviting_corporation is not None:
        usr.corporation = state_code.inviting_corporation
        usr.clearance_level = -1
        usr.save()

    if not is_authorized_to_login(usr):
        return not_authorized_to_login_response(
            usr.character_name, usr.character_id
        )
    if not token_has_enough_scopes(access_token, usr):
        return not_enough_scopes_response(
            usr.character_name,
            usr.character_id,
            list(usr.cumulated_mandatory_esi_scopes()),
            access_token.scp,
        )

    user_token = create_user_token(state_code.app_token, usr)
    user_jwt_str = to_jwt(user_token)
    logging.info(
        "Issuing token %s to app %s", user_jwt_str, state_code.app_token.uuid
    )

    if state_code.app_token.callback is None:
        return {
            "created_on": user_token.created_on,
            "expires_on": user_token.expires_on,
            "jwt": user_jwt_str,
            "owner": {
                "character_id": user_token.owner.character_id,
                "character_name": user_token.owner.character_name,
                "clearance_level": user_token.owner.clearance_level,
            },
        }

    request = requests.Request(
        "GET",
        state_code.app_token.callback,
        params={
            "state_code": str(state_code.uuid),
            "user_token": user_jwt_str,
        },
    )
    url = request.prepare().url
    if url is None:
        logging.error(
            "Failed to redirect user to %s", state_code.app_token.callback,
        )
        return PlainTextResponse(
            f"Failed to redirect to {state_code.app_token.callback}"
        )
    return RedirectResponse(url=url)
