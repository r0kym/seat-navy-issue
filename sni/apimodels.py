# pylint: disable=no-member
# pylint: disable=too-few-public-methods
"""
Body models for the API server
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

import pydantic

import sni.dbmodels as dbmodels


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
