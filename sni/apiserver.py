# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
"""
API Server
"""

import logging
import traceback

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    status,
)
from fastapi.responses import JSONResponse
import mongoengine
import requests

from sni.apimodels import *
import sni.conf as conf
import sni.dbmodels as dbmodels
import sni.esi as esi
import sni.time as time
import sni.token as token

app = FastAPI()


@app.exception_handler(mongoengine.DoesNotExist)
def does_not_exist_exception_handler(_request: requests.Request,
                                     error: Exception):
    """
    Catches :class:`mongoengine.DoesNotExist` exceptions and forwards them as
    ``404``'s.
    """
    content = None
    if conf.get('general.debug'):
        content = {'details': str(error)}
    return JSONResponse(
        content=content,
        status_code=status.HTTP_404_NOT_FOUND,
    )


@app.exception_handler(Exception)
def exception_handler(_request: requests.Request, error: Exception):
    """
    Global exception handler.

    Prints trace for all others.
    """
    if conf.get('general.debug'):
        traceback_data = traceback.format_exception(
            etype=type(error),
            value=error,
            tb=error.__traceback__,
        )
        logging.error(''.join(traceback_data))


@app.get(
    '/callback/esi',
    tags=['Callbacks'],
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


@app.get('/esi/latest/{esi_path:path}', tags=['ESI'])
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
        esi_token = dbmodels.EsiToken.objects.get(
            owner=user,
            scopes='esi-assets.read_assets.v1',
            expires_on__gt=time.now(),
        )
        headers['Authorization'] = 'Bearer ' + esi_token.access_token
    response_json = requests.get(
        'https://esi.evetech.net/latest/' + esi_path,
        headers=headers,
        params=data.params,
    ).json()
    return response_json


@app.get(
    '/ping',
    tags=['Testing'],
)
async def get_ping():
    """
    Returns ``pong``.
    """
    return 'pong'


@app.delete('/token')
async def delete_token(
        uuid: str,
        app_token: dbmodels.Token = Depends(token.validate_header),
):
    """
    Deletes a token
    """
    if not app_token.owner.character_id == 0:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    if not token.delete_token(uuid):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail='Token not found.')


@app.get(
    '/token',
    response_model=GetTokenOut,
)
async def get_token(app_token: dbmodels.Token = Depends(
    token.validate_header)):
    """
    Returns informations about the token currently being used.
    """
    return GetTokenOut(
        callback=app_token.callback,
        comments=app_token.comments,
        created_on=app_token.created_on,
        expires_on=app_token.expires_on,
        owner_character_id=app_token.owner.character_id,
        parent=app_token.parent,
        token_type=app_token.token_type,
        uuid=str(app_token.uuid),
    )


@app.post(
    '/token/dyn',
    response_model=PostTokenDynOut,
    tags=['Authentication'],
)
async def post_token_dyn(
        data: PostTokenDynIn,
        app_token: dbmodels.Token = Depends(token.validate_header),
):
    """
    Creates a new dynamic app token.

    Must be called with a permanent app token.
    """
    if app_token.token_type != dbmodels.Token.TokenType.per:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    new_token = token.create_dynamic_app_token(
        app_token.owner,
        callback=data.callback,
        comments=data.comments,
        parent=app_token,
    )
    return PostTokenDynOut(app_token=token.to_jwt(new_token))


@app.post(
    '/token/per',
    response_model=PostTokenPerOut,
    tags=['Authentication'],
)
async def post_token_per(
        data: PostTokenPerIn,
        app_token: dbmodels.Token = Depends(token.validate_header),
):
    """
    Creates a new permanent app token.

    Must be called with a permanent app token.
    """
    if app_token.token_type != dbmodels.Token.TokenType.per:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    new_token = token.create_permanent_app_token(
        app_token.owner,
        callback=data.callback,
        comments=data.comments,
        parent=app_token,
    )
    return PostTokenPerOut(app_token=token.to_jwt(new_token))


@app.post(
    '/token/use/from/dyn',
    response_model=PostTokenUseFromDynOut,
    tags=['Authentication'],
)
async def post_token_use_from_dyn(
        data: PostTokenUseFromDynIn,
        app_token: dbmodels.Token = Depends(token.validate_header),
):
    """
    Authenticates an application dynamic token and returns a `state code` and
    an URL at which the user can authenticate to the EVE SSO. Once that is
    done, SNI issues a GET request to the app predefined callback, with that
    state code and the user token.
    """
    if app_token.token_type != dbmodels.Token.TokenType.dyn:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    state_code = token.create_state_code(app_token)
    return PostTokenUseFromDynOut(
        login_url=esi.get_auth_url(data.scopes, str(state_code.uuid)),
        state_code=str(state_code.uuid),
    )


@app.post(
    '/token/use/from/per',
    response_model=PostUseFromPerOut,
    tags=['Authentication'],
)
async def post_token_use_from_per(app_token: dbmodels.Token = Depends(
    token.validate_header)):
    """
    Authenticates an application permanent token and returns a user token tied
    to the owner of that app token.
    """
    if app_token.token_type != dbmodels.Token.TokenType.per:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    user_token = token.create_user_token(app_token)
    user_token_str = token.to_jwt(user_token)
    return PostUseFromPerOut(user_token=user_token_str)
