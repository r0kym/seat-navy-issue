# pylint: disable=no-member
# pylint: disable=too-few-public-methods
"""
Body models for the API server
"""

from typing import List

import pydantic


class AuthDynIn(pydantic.BaseModel):
    """
    Model for ``/auth/dyn`` requests.
    """
    scopes: List[str] = pydantic.Field(['publicData'])


class AuthDynOut(pydantic.BaseModel):
    """
    Model for ``/auth/dyn`` reponses.
    """
    login_url: str
    state_code: str


class AuthPerOut(pydantic.BaseModel):
    """
    Model for ``/auth/per`` reponses.
    """
    user_token: str
