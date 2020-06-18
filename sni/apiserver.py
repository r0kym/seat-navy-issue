"""
API Server
"""

import logging
from uuid import uuid4

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    status,
)

import sni.apimodels as apimodels
from sni.dbmodels import Token
import sni.esi as esi
import sni.token as token

app = FastAPI()


@app.get(
    '/auth/dyn',
    response_model=apimodels.GetAuthDynOut,
    status_code=status.HTTP_200_OK,
    tags=['Authentication'],
)
async def get_auth_dyn(data: apimodels.GetAuthDynIn,
                       app_token: Token = Depends(token.validate_header)):
    """
    Authenticates an application dynamic token and returns a `state code` and
    an URL at which the user can authenticate to the EVE SSO. Once that is
    done, SNI issues a GET request to the app predefined callback, with that
    state code and the user token.
    """
    if app_token.token_type != 'dyn':
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    state_code = str(uuid4())
    return apimodels.GetAuthDynOut(
        login_url=esi.get_auth_url(data.scopes, state_code),
        state_code=state_code,
    )


@app.get(
    '/auth/per',
    response_model=apimodels.GetAuthPerOut,
    status_code=status.HTTP_200_OK,
    tags=['Authentication'],
)
async def get_auth_per(app_token: Token = Depends(token.validate_header)):
    """
    Authenticates an application permanent token and returns a user token tied
    to the owner of that app token.
    """
    if app_token.token_type != 'per':
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    user_token = token.create_user_token(app_token)
    user_token_str = token.to_jwt(user_token)
    return apimodels.GetAuthPerOut(user_token=user_token_str)


@app.get(
    '/callback/esi',
    status_code=status.HTTP_200_OK,
    tags=['Callbacks'],
)
async def get_callback_esi(code: str, state: str):
    """
    ESI callback.
    """
    logging.info('Received callback from ESI for state %s', state)
    if not esi.process_sso_authorization_code(code, state):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Could not obtain or validate access token from ESI',
        )


@app.get('/ping', tags=['Testing'])
async def get_ping():
    """
    Returns ``pong``.
    """
    return 'pong'
