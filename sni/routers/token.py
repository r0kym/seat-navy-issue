# pylint: disable=no-member
# pylint: disable=too-few-public-methods
"""
Token management paths
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
import pydantic

import sni.dbmodels as dbmodels
import sni.esi.sso as sso
import sni.token as token

router = APIRouter()


class GetTokenOut(pydantic.BaseModel):
    """
    Model for ``GET /token`` responses.
    """
    callback: Optional[pydantic.AnyHttpUrl]
    comments: Optional[str]
    created_on: datetime
    expires_on: Optional[datetime]
    owner_character_id: int
    parent: Optional[UUID]
    token_type: dbmodels.Token.TokenType
    uuid: UUID


class PostTokenUseFromDynIn(pydantic.BaseModel):
    """
    Model for ``POST /token/use/from/dyn`` requests.
    """
    scopes: List[str] = pydantic.Field(['publicData'])


class PostTokenUseFromDynOut(pydantic.BaseModel):
    """
    Model for ``POST /token/use/from/dyn`` reponses.
    """
    login_url: str
    state_code: str


class PostUseFromPerOut(pydantic.BaseModel):
    """
    Model for ``POST /token/use/from/per`` reponses.
    """
    user_token: str


class PostTokenDynIn(pydantic.BaseModel):
    """
    Model for ``POST /token/dyn`` requests.
    """
    callback: pydantic.AnyHttpUrl
    comments: Optional[str]


class PostTokenDynOut(pydantic.BaseModel):
    """
    Model for ``POST /token/dyn`` reponses.
    """
    app_token: str


class PostTokenPerIn(pydantic.BaseModel):
    """
    Model for ``POST /token/per`` requests.
    """
    callback: pydantic.AnyHttpUrl
    comments: Optional[str]


class PostTokenPerOut(pydantic.BaseModel):
    """
    Model for ``POST /token/per`` reponses.
    """
    app_token: str


@router.delete('/token')
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


@router.get(
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


@router.post(
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


@router.post(
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


@router.post(
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
        login_url=sso.get_auth_url(data.scopes, str(state_code.uuid)),
        state_code=str(state_code.uuid),
    )


@router.post(
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
