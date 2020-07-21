"""
ESI related paths
"""

import logging
from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.responses import PlainTextResponse, RedirectResponse
import pydantic
import requests

from sni.user.models import User

from sni.esi.esi import (
    esi_get,
    EsiResponse,
    get_esi_path_scope,
)
from sni.esi.sso import (
    decode_access_token,
    get_access_token_from_callback_code,
)
from sni.esi.token import (
    get_access_token,
    save_esi_tokens,
)
from sni.uac.clearance import assert_has_clearance
from sni.uac.token import (
    create_user_token,
    from_authotization_header_nondyn,
    StateCode,
    to_jwt,
    Token,
)
from sni.uac.uac import is_authorized_to_login

router = APIRouter()


class EsiRequestIn(pydantic.BaseModel):
    """
    Data to be forwarded to the ESI
    """
    on_behalf_of: Optional[int] = None
    params: dict = {}


@router.get(
    '/callback/esi',
    summary='ESI callback',
    tags=['Callbacks', 'ESI'],
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
    logging.info('Received callback from ESI for state %s', state)

    state_code: StateCode = StateCode.objects.get(uuid=state)
    state_code.delete()
    esi_response = get_access_token_from_callback_code(code)
    decoded_access_token = decode_access_token(esi_response.access_token)
    save_esi_tokens(esi_response)

    usr: User = User.objects.get(
        character_id=decoded_access_token.character_id)
    if not is_authorized_to_login(usr):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail=f'Character {usr.character_name} ({usr.character_id}) ' \
                + 'is not allowed to login.',
        )
    if not usr.cumulated_mandatory_esi_scopes() <= set(
            decoded_access_token.scp):
        detail = f'Insufficient scopes for character {usr.character_name} ' \
                + f'({usr.character_id}). Require at least: ' \
                + ', '.join(list(usr.cumulated_mandatory_esi_scopes()))
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=detail)

    user_token = create_user_token(state_code.app_token, usr)
    user_jwt_str = to_jwt(user_token)
    logging.info('Issuing token %s to app %s', user_jwt_str,
                 state_code.app_token.uuid)
    if state_code.app_token.callback is None:
        return PlainTextResponse(content='Authentication successful')
    request = requests.Request(
        'GET',
        state_code.app_token.callback,
        params={
            'state_code': str(state_code.uuid),
            'user_token': user_jwt_str,
        },
    )
    url = request.prepare().url
    if url is None:
        logging.error(
            'Failed to redirect user to %s',
            state_code.app_token.callback,
        )
        return PlainTextResponse(
            f'Failed to redirect to {state_code.app_token.callback}')
    return RedirectResponse(url=url)


@router.get(
    '/esi/{esi_path:path}',
    response_model=EsiResponse,
    summary='Proxy path to the ESI',
    tags=['ESI'],
)
async def get_esi_latest(
        esi_path: str,
        data: EsiRequestIn = EsiRequestIn(),
        tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Forwards a `GET` request to the ESI. The required clearance level depends
    on the user making the request and the user specified on the
    `on_behalf_of` field. See also `EsiRequestIn`.
    """
    esi_token: Optional[str] = None
    if data.on_behalf_of:
        esi_scope = get_esi_path_scope(esi_path)
        if esi_scope is not None:
            target = User.objects.get(character_id=data.on_behalf_of)
            assert_has_clearance(tkn.owner, esi_scope, target)
            esi_token = get_access_token(
                data.on_behalf_of,
                esi_scope,
            ).access_token
    return esi_get(esi_path, esi_token, params=data.params)
