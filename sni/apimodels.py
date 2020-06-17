# pylint: disable=no-member
# pylint: disable=too-few-public-methods
"""
Body models for the API server
"""

from typing import List

import pydantic


class AuthIn(pydantic.BaseModel):
    """
    Model for ``/auth`` requests.
    """
    scopes: List[str] = pydantic.Field(['publicData'])


class AuthOut(pydantic.BaseModel):
    """
    Model for ``/auth`` reponses.
    """
    login_url: str
    user_token: str
    user_token_valid: bool
