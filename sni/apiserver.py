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

from sni.apimodels import (
    PostAuthDynIn,
    PostAuthDynOut,
    PostAuthPerOut,
    PostTokenIn,
    PostTokenOut,
)
from sni.dbmodels import Token
import sni.esi as esi
import sni.token as token

app = FastAPI()


@app.post(
    '/auth/dyn',
    response_model=PostAuthDynOut,
    status_code=status.HTTP_200_OK,
    tags=['Authentication'],
)
async def post_auth_dyn(data: PostAuthDynIn,
                        app_token: Token = Depends(token.validate_header)):
    """
    Authenticates an application dynamic token and returns a `state code` and
    an URL at which the user can authenticate to the EVE SSO. Once that is
    done, SNI issues a GET request to the app predefined callback, with that
    state code and the user token.
    """
    if app_token.token_type != Token.TokenType.dyn:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    state_code = str(uuid4())
    return PostAuthDynOut(
        login_url=esi.get_auth_url(data.scopes, state_code),
        state_code=state_code,
    )


@app.post(
    '/auth/per',
    response_model=PostAuthPerOut,
    status_code=status.HTTP_200_OK,
    tags=['Authentication'],
)
async def post_auth_per(app_token: Token = Depends(token.validate_header)):
    """
    Authenticates an application permanent token and returns a user token tied
    to the owner of that app token.
    """
    if app_token.token_type != Token.TokenType.per:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    user_token = token.create_user_token(app_token)
    user_token_str = token.to_jwt(user_token)
    return PostAuthPerOut(user_token=user_token_str)


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


@app.get(
    '/ping',
    tags=['Testing'],
)
async def get_ping():
    """
    Returns ``pong``.
    """
    return 'pong'


@app.post(
    '/token',
    tags=['Authentication'],
    response_model=PostTokenOut,
)
async def post_token(data: PostTokenIn,
                     app_token: Token = Depends(token.validate_header)):
    """
    Creates a new app token of any type.

    Must be called with a permanent app token.
    """
    if app_token.token_type != Token.TokenType.per:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    if data.token_type == Token.TokenType.dyn:
        new_token = token.create_dynamic_app_token(
            app_token.owner,
            data.callback,
        )
        return PostTokenOut(
            app_token=token.to_jwt(new_token)
        )
    if data.token_type == Token.TokenType.per:
        new_token = token.create_permanent_app_token(
            app_token.owner,
            data.callback,
        )
        return PostTokenOut(
            app_token=token.to_jwt(new_token)
        )
    raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                        'This enpoint can only create app tokens.')
