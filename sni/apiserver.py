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
    PostTokenUseFromDynIn,
    PostTokenUseFromDynOut,
    PostUseFromPerOut,
    PostTokenDynIn,
    PostTokenDynOut,
    PostTokenPerIn,
    PostTokenPerOut,
)
from sni.dbmodels import Token
import sni.esi as esi
import sni.token as token

app = FastAPI()


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
    '/token/dyn',
    response_model=PostTokenDynOut,
    tags=['Authentication'],
)
async def post_token_dyn(
        data: PostTokenDynIn,
        app_token: Token = Depends(token.validate_header),
):
    """
    Creates a new dynamic app token.

    Must be called with a permanent app token.
    """
    if app_token.token_type != Token.TokenType.per:
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
        app_token: Token = Depends(token.validate_header),
):
    """
    Creates a new permanent app token.

    Must be called with a permanent app token.
    """
    if app_token.token_type != Token.TokenType.per:
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
    status_code=status.HTTP_200_OK,
    tags=['Authentication'],
)
async def post_token_use_from_dyn(
        data: PostTokenUseFromDynIn,
        app_token: Token = Depends(token.validate_header),
):
    """
    Authenticates an application dynamic token and returns a `state code` and
    an URL at which the user can authenticate to the EVE SSO. Once that is
    done, SNI issues a GET request to the app predefined callback, with that
    state code and the user token.
    """
    if app_token.token_type != Token.TokenType.dyn:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    state_code = str(uuid4())
    return PostTokenUseFromDynOut(
        login_url=esi.get_auth_url(data.scopes, state_code),
        state_code=state_code,
    )


@app.post(
    '/token/use/from/per',
    response_model=PostUseFromPerOut,
    status_code=status.HTTP_200_OK,
    tags=['Authentication'],
)
async def post_token_use_from_per(app_token: Token = Depends(
    token.validate_header)):
    """
    Authenticates an application permanent token and returns a user token tied
    to the owner of that app token.
    """
    if app_token.token_type != Token.TokenType.per:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    user_token = token.create_user_token(app_token)
    user_token_str = token.to_jwt(user_token)
    return PostUseFromPerOut(user_token=user_token_str)
