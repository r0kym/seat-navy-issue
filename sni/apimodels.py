# pylint: disable=no-member
# pylint: disable=too-few-public-methods
"""
Body models for the API server
"""

from typing import List, Optional

import pydantic


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
