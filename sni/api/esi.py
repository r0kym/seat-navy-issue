"""
ESI related paths
"""

import logging
from typing import Any, Optional

from fastapi import (
    APIRouter,
    Depends,
)
import pydantic
import requests

import sni.esi.esi as esi
import sni.esi.sso as sso
import sni.esi.token as esitoken
import sni.uac.clearance as clearance
import sni.uac.token as snitoken
import sni.user.user as user

router = APIRouter()


class EsiRequestIn(pydantic.BaseModel):
    """
    Data to be forwarded to the ESI
    """
    on_behalf_of: Optional[int] = None
    params: dict = {}


class EsiRequestOut(pydantic.BaseModel):
    """
    SNI response to an ESI request
    """
    data: Any
    headers: Optional[dict]
    status_code: int


class PostCallbackEsiOut(pydantic.BaseModel):
    """
    Notification model to the app when receiving a callback from the ESI.
    """
    state_code: str
    user_token: str


@router.get(
    '/callback/esi',
    summary='ESI callback',
    tags=['Callbacks', 'ESI'],
)
async def get_callback_esi(code: str, state: str):
    """
    ESI callback. You should not manually call this.

    Upon receiving a notification from EVE SSO, SNI notifies the appropriate
    app by issuing a `POST` request to the predefined app callback, using the
    `PostCallbackEsiOut` model.

    Reference: OAuth 2.0 for Web Based Applications
    https://docs.esi.evetech.net/docs/sso/web_based_sso_flow.html
    """
    logging.info('Received callback from ESI for state %s', state)
    state_code: snitoken.StateCode = snitoken.StateCode.objects.get(uuid=state)
    esi_response = sso.get_access_token(code)
    decoded_access_token = sso.decode_access_token(esi_response.access_token)
    esitoken.save_esi_tokens(esi_response)
    user_token = snitoken.create_user_token(
        state_code.app_token,
        user.User.objects.get(character_id=decoded_access_token.character_id))
    user_jwt_str = snitoken.to_jwt(user_token)
    logging.info('Issuing token %s to app %s', user_jwt_str,
                 state_code.app_token.uuid)
    try:
        requests.post(
            state_code.app_token.callback,
            data=PostCallbackEsiOut(
                state_code=str(state_code.uuid),
                user_token=user_jwt_str,
            ),
        )
    except Exception as error:
        logging.error('Failed to notify app %s: %s', state_code.app_token.uuid,
                      str(error))
    state_code.delete()


@router.get(
    '/esi/{esi_path:path}',
    response_model=EsiRequestOut,
    summary='Proxy path to the ESI',
    tags=['ESI'],
)
async def get_esi_latest(
    esi_path: str,
    data: EsiRequestIn = EsiRequestIn(),
    tkn: snitoken.Token = Depends(snitoken.from_authotization_header_nondyn),
):
    """
    Forwards a `GET` request to the ESI. The required clearance level depends
    on the user making the request and the user specified on the
    `on_behalf_of` field. See also `EsiRequestIn`.
    """
    esi_token: Optional[str] = None
    if data.on_behalf_of:
        esi_scope = esi.get_path_scope(esi_path)
        if esi_scope is not None:
            target = user.User.objects.get(character_id=data.on_behalf_of)
            clearance.assert_has_clearance(tkn.owner, esi_scope, target)
            esi_token = esitoken.get_access_token(
                data.on_behalf_of,
                esi_scope,
            ).access_token
    response = esi.get(
        esi_path,
        esi_token,
        params=data.params,
    )
    return EsiRequestOut(
        data=response.json(),
        headers=response.headers,
        status_code=response.status_code,
    )
