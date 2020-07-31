"""
Teamspeak related paths
"""

from datetime import datetime
from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
import mongoengine as me
import pydantic as pdt

from sni.teamspeak.teamspeak import (
    complete_authentication_challenge,
    new_authentication_challenge,
    new_teamspeak_connection,
)
import sni.utils as utils
from sni.uac.clearance import assert_has_clearance
from sni.uac.token import (
    from_authotization_header_nondyn,
    Token,
)

router = APIRouter()


class PostAuthStartOut(pdt.BaseModel):
    """
    Model for `POST /teamspeak/auth/start` responses.
    """

    expiration_datetime: datetime
    challenge_nickname: str
    user: str


@router.post(
    "/auth/start",
    response_model=PostAuthStartOut,
    summary="Starts a teamspeak authentication challenge",
)
def port_auth_start(tkn: Token = Depends(from_authotization_header_nondyn)):
    """
    Starts a new authentication challenge for the owner of the token. A random
    nickname is returned (see `PostAuthStartOut` for more details), and the
    user has 1 minute to update its teamspeak nickname to it, and then call
    `POST /teamspeak/auth/complete`.
    """
    assert_has_clearance(tkn.owner, "sni.teamspeak.auth")
    return PostAuthStartOut(
        expiration_datetime=utils.now_plus(seconds=60),
        challenge_nickname=new_authentication_challenge(tkn.owner),
        user=tkn.owner.character_name,
    )


@router.post(
    "/auth/complete",
    status_code=status.HTTP_201_CREATED,
    summary="Completes a teamspeak authentication challenge",
)
def post_auth_complete(tkn: Token = Depends(from_authotization_header_nondyn)):
    """
    Completes an authentication challenge for the owner of the token. See the
    `POST /teamspeak/auth/start` documentation.
    """
    assert_has_clearance(tkn.owner, "sni.teamspeak.auth")
    exception: Optional[HTTPException] = None
    try:
        connection = new_teamspeak_connection()
        complete_authentication_challenge(connection, tkn.owner)
    except LookupError:
        exception = HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Could not find corresponding teamspeak client",
        )
    except me.DoesNotExist:
        exception = HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Could not find challenge for user",
        )
    connection.close()
    if exception is not None:
        raise exception
