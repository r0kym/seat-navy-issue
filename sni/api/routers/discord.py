"""
Discord related API methods
"""

from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
)
import pydantic as pdt

from sni.discord.discord import new_authentication_challenge
import sni.utils as utils
from sni.uac.clearance import assert_has_clearance
from sni.uac.token import (
    from_authotization_header_nondyn,
    Token,
)

from .user import GetUserShortOut

router = APIRouter()


class PostAuthStartOut(pdt.BaseModel):
    """
    Model for `POST /discord/auth/start` responses.
    """

    code: str
    expiration_datetime: datetime
    user: GetUserShortOut


@router.post(
    "/auth/start",
    response_model=PostAuthStartOut,
    summary="Starts a Discord authentication challenge",
)
def port_auth_start(tkn: Token = Depends(from_authotization_header_nondyn)):
    """
    Starts a new authentication challenge for the owner of the token. A random
    code is returned (see `PostAuthStartOut` for more details), and the user
    has 1 minute to post it as `!auth <code>` in the dedicated authentication
    chanel.
    """
    assert_has_clearance(tkn.owner, "sni.discord.auth")
    return PostAuthStartOut(
        expiration_datetime=utils.now_plus(seconds=60),
        code=new_authentication_challenge(tkn.owner),
        user=GetUserShortOut.from_record(tkn.owner),
    )
