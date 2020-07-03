"""
Token management paths
"""

from datetime import datetime
import logging
from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
import pydantic as pdt

import sni.esi.sso as sso
import sni.uac.clearance as clearance
import sni.uac.token as token
import sni.uac.user as user

router = APIRouter()


class GetTokenOut(pdt.BaseModel):
    """
    Model for ``GET /token`` responses.
    """
    callback: Optional[pdt.AnyHttpUrl]
    comments: Optional[str]
    created_on: datetime
    expires_on: Optional[datetime]
    owner_character_id: int
    owner_character_name: str
    parent: Optional[str]
    token_type: token.Token.TokenType
    uuid: str


class PostTokenUseFromDynIn(pdt.BaseModel):
    """
    Model for ``POST /token/use/from/dyn`` requests.
    """
    scopes: List[str] = pdt.Field(['publicData'])


class PostTokenUseFromDynOut(pdt.BaseModel):
    """
    Model for ``POST /token/use/from/dyn`` reponses.
    """
    login_url: str
    state_code: str


class PostUseFromPerOut(pdt.BaseModel):
    """
    Model for ``POST /token/use/from/per`` reponses.
    """
    user_token: str


class PostTokenDynIn(pdt.BaseModel):
    """
    Model for ``POST /token/dyn`` requests.
    """
    callback: pdt.AnyHttpUrl
    comments: Optional[str]


class PostTokenDynOut(pdt.BaseModel):
    """
    Model for ``POST /token/dyn`` reponses.
    """
    tkn: str


class PostTokenPerIn(pdt.BaseModel):
    """
    Model for ``POST /token/per`` requests.
    """
    callback: pdt.AnyHttpUrl
    comments: Optional[str]


class PostTokenPerOut(pdt.BaseModel):
    """
    Model for ``POST /token/per`` reponses.
    """
    tkn: str


@router.delete(
    '',
    summary='Manually delete a token',
)
async def delete_token(
        uuid: str,
        tkn: token.Token = Depends(token.from_authotization_header_nondyn),
):
    """
    Manually deletes a token (of any type). Requires a clearance level of 10.
    """
    tok: token.Token = token.Token.objects.get(uuid=uuid)
    if tok.token_type == token.Token.TokenType.dyn:
        clearance.assert_has_clearance(tkn.owner, 'sni.delete_dyn_token')
    elif tok.token_type == token.Token.TokenType.per:
        clearance.assert_has_clearance(tkn.owner, 'sni.delete_per_token')
    elif tok.token_type == token.Token.TokenType.use:
        clearance.assert_has_clearance(tkn.owner, 'sni.delete_use_token')
    else:
        logging.error('Token %s has unknown type %s', tok.uuid, tok.token_type)
        raise PermissionError
    tok.delete()
    logging.debug('Deleted token %s', uuid)


@router.get(
    '',
    response_model=GetTokenOut,
    summary='Get basic informations about the current token',
)
async def get_token(tkn: token.Token = Depends(
    token.from_authotization_header_nondyn)):
    """
    Returns informations about the token currently being used. Requires a
    clearance level of 0 or more.
    """
    clearance.assert_has_clearance(tkn.owner, 'sni.read_own_token')
    return GetTokenOut(
        callback=tkn.callback,
        comments=tkn.comments,
        created_on=tkn.created_on,
        expires_on=tkn.expires_on,
        owner_character_id=tkn.owner.character_id,
        owner_character_name=tkn.owner.character_name,
        parent=str(tkn.parent.uuid),
        token_type=tkn.token_type,
        uuid=str(tkn.uuid),
    )


@router.post(
    '/dyn',
    response_model=PostTokenDynOut,
    summary='Create a new dynamic app token',
)
async def post_token_dyn(
        data: PostTokenDynIn,
        tkn: token.Token = Depends(token.from_authotization_header_nondyn),
):
    """
    Creates a new dynamic app token. Must be called with a permanent app token,
    and the owner must have a clearance level of 10.
    """
    clearance.assert_has_clearance(tkn.owner, 'sni.create_dyn_token')
    if tkn.token_type != token.Token.TokenType.per:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    new_token = token.create_dynamic_app_token(
        tkn.owner,
        callback=data.callback,
        comments=data.comments,
        parent=tkn,
    )
    return PostTokenDynOut(tkn=token.to_jwt(new_token))


@router.post(
    '/per',
    response_model=PostTokenPerOut,
    summary='Create a new permanent app token',
)
async def post_token_per(
        data: PostTokenPerIn,
        tkn: token.Token = Depends(token.from_authotization_header_nondyn),
):
    """
    Creates a new permanent app token. Must be called with a permanent app
    token, and the owner must have a clearance level of 10.
    """
    clearance.assert_has_clearance(tkn.owner, 'sni.create_per_token')
    if tkn.token_type != token.Token.TokenType.per:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    new_token = token.create_permanent_app_token(
        tkn.owner,
        callback=data.callback,
        comments=data.comments,
        parent=tkn,
    )
    return PostTokenPerOut(tkn=token.to_jwt(new_token))


@router.post(
    '/use/from/dyn',
    response_model=PostTokenUseFromDynOut,
    summary='Create a new user token with a dynamic app token',
)
async def post_token_use_from_dyn(
        data: PostTokenUseFromDynIn,
        tkn: token.Token = Depends(token.from_authotization_header),
):
    """
    Authenticates an application dynamic token and returns a `state code` and
    an URL at which the user can authenticate to the EVE SSO. Once that is
    done, SNI issues a GET request to the app predefined callback, with that
    state code and the user token. Requires the owner of the token to have a
    clearance level of 0 or more.
    """
    if tkn.token_type != token.Token.TokenType.dyn:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail='Must use a dynamic app token for this path.')
    clearance.assert_has_clearance(tkn.owner, 'sni.create_use_token')
    state_code = token.create_state_code(tkn)
    return PostTokenUseFromDynOut(
        login_url=sso.get_auth_url(data.scopes, str(state_code.uuid)),
        state_code=str(state_code.uuid),
    )


@router.post(
    '/use/from/per',
    response_model=PostUseFromPerOut,
    summary='Create a new user token with a permanent app token',
)
async def post_token_use_from_per(tkn: token.Token = Depends(
    token.from_authotization_header)):
    """
    Authenticates an application permanent token and returns a user token tied
    to the owner of that app token.
    """
    if tkn.token_type != token.Token.TokenType.per:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail='Must use a permanent app token for this path.')
    clearance.assert_has_clearance(tkn.owner, 'sni.create_use_token')
    user_token = token.create_user_token(
        tkn,
        user.User.objects.get(character_id=0),
    )
    user_token_str = token.to_jwt(user_token)
    return PostUseFromPerOut(user_token=user_token_str)
