# pylint: disable=no-member
# pylint: disable=too-few-public-methods
"""
Body models for the API server
"""

from typing import List

import pydantic


class GetAuthDynIn(pydantic.BaseModel):
    """
    Model for ``GET /auth/dyn`` requests.
    """
    scopes: List[str] = pydantic.Field(['publicData'])


class GetAuthDynOut(pydantic.BaseModel):
    """
    Model for ``GET /auth/dyn`` reponses.
    """
    login_url: str
    state_code: str


class GetAuthPerOut(pydantic.BaseModel):
    """
    Model for ``GET /auth/per`` reponses.
    """
    user_token: str
