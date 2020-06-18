# pylint: disable=no-member
# pylint: disable=too-few-public-methods
"""
Body models for the API server
"""

from typing import List

import pydantic

import sni.dbmodels as dbmodels


class PostAuthDynIn(pydantic.BaseModel):
    """
    Model for ``POST /auth/dyn`` requests.
    """
    scopes: List[str] = pydantic.Field(['publicData'])


class PostAuthDynOut(pydantic.BaseModel):
    """
    Model for ``POST /auth/dyn`` reponses.
    """
    login_url: str
    state_code: str


class PostAuthPerOut(pydantic.BaseModel):
    """
    Model for ``POST /auth/per`` reponses.
    """
    user_token: str


class PostTokenIn(pydantic.BaseModel):
    """
    Model for ``POST /token`` requests.
    """
    callback: pydantic.AnyHttpUrl
    token_type: dbmodels.Token.TokenType


class PostTokenOut(pydantic.BaseModel):
    """
    Model for ``POST /token`` reponses.
    """
    app_token: str
