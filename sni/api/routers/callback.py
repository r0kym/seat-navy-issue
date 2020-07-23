"""
Callback paths
"""

import logging

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import PlainTextResponse, RedirectResponse
import requests

from sni.user.models import User

from sni.esi.sso import (
    decode_access_token,
    get_access_token_from_callback_code,
)
from sni.esi.token import save_esi_tokens, token_has_enough_scopes
from sni.uac.token import create_user_token, StateCode, to_jwt
from sni.uac.uac import is_authorized_to_login

router = APIRouter()


@router.get(
    '/esi',
    summary='ESI callback',
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
    access_token = decode_access_token(esi_response.access_token)
    save_esi_tokens(esi_response)

    usr: User = User.objects.get(character_id=access_token.character_id)
    if not is_authorized_to_login(usr):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail=f'Character {usr.character_name} ({usr.character_id}) ' \
                + 'is not allowed to login.',
        )
    if not token_has_enough_scopes(access_token, usr):
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
