# pylint: disable=no-member
# pylint: disable=too-few-public-methods
"""
ESI related paths
"""

import logging
from typing import Any, Optional

from fastapi import (
    APIRouter,
    Depends,
)
import mongoengine
import pydantic
import requests

import sni.conf as conf
import sni.dbmodels as dbmodels
import sni.esi as esi
import sni.time as time
import sni.token as token

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
    tags=['Callbacks', 'ESI'],
)
async def get_callback_esi(code: str, state: str):
    """
    ESI callback.

    Notifies the app with by issuing a POST request to the predefined app
    callback, using the :class:`sni.apimodels.PostCallbackEsiOut` model.

    Reference:
        `OAuth 2.0 for Web Based Applications <https://docs.esi.evetech.net/docs/sso/web_based_sso_flow.html>`_
    """
    logging.info('Received callback from ESI for state %s', state)
    esi_response = esi.get_access_token(code)
    decoded_access_token = esi.decode_access_token(esi_response.access_token)
    state_code = dbmodels.StateCode.objects.get(uuid=state)
    try:
        user = dbmodels.User.objects.get(
            character_id=decoded_access_token.character_id)
    except mongoengine.DoesNotExist:
        user = dbmodels.User(
            character_id=decoded_access_token.character_id,
            character_name=decoded_access_token.name,
        ).save()
    dbmodels.EsiToken(
        access_token=esi_response.access_token,
        app_token=state_code.app_token,
        expires_on=time.from_timestamp(decoded_access_token.exp),
        owner=user,
        refresh_token=esi_response.refresh_token,
        scopes=decoded_access_token.scp,
    ).save()
    user_token = token.create_user_token(state_code.app_token)
    user_jwt_str = token.to_jwt(user_token)
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
    except Exception as error:  # pylint: disable=broad-except
        logging.error('Failed to notify app %s: %s', state_code.app_token.uuid,
                      str(error))
    state_code.delete()


@router.get(
    '/esi/{esi_path:path}',
    tags=['ESI'],
    response_model=EsiRequestOut,
)
async def get_esi_latest(
        esi_path: str,
        data: EsiRequestIn = EsiRequestIn(),
        app_token: dbmodels.Token = Depends(token.validate_header),
):
    """
    Forwards a GET request to the ESI.

    See also:
        :class:`sni.apimodels.EsiRequestIn`
    """
    headers = {
        'Accept-Encoding': 'gzip',
        'accept': 'application/json',
        'User-Agent': 'SeAT Navy Issue @ ' + conf.get('general.root_url'),
    }
    if data.on_behalf_of:
        user = dbmodels.User.objects.get(character_id=data.on_behalf_of)
        scope = esi.get_path_scope(esi_path)
        esi_token = dbmodels.EsiToken.objects.get(
            owner=user,
            scopes=scope,
            expires_on__gt=time.now(),
        )
        headers['Authorization'] = 'Bearer ' + esi_token.access_token
    response = requests.get(
        'https://esi.evetech.net/' + esi_path,
        headers=headers,
        params=data.params,
    )
    return EsiRequestOut(
        data=response.json(),
        headers=response.headers,
        status_code=response.status_code,
    )
