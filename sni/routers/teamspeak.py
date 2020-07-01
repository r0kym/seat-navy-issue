"""
Teamspeak related paths
"""

from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
import mongoengine as me
import pydantic as pdt

import sni.teamspeak as teamspeak
import sni.time as time
import sni.uac.token as token

router = APIRouter()


class PostAuthStartOut(pdt.BaseModel):
    """
    Model for ``POST /teamspeak/auth/start`` responses
    """
    expiration_datetime: datetime
    challenge_nickname: str
    user: str


@router.post('/auth/start', response_model=PostAuthStartOut)
def port_auth_start(tkn: token.Token = Depends(
    token.from_authotization_header_nondyn)):
    """
    Starts a new authentication challenge for the owner of the token.
    """
    return PostAuthStartOut(
        expiration_datetime=time.now_plus(seconds=60),
        challenge_nickname=teamspeak.new_authentication_challenge(tkn.owner),
        user=tkn.owner.character_name,
    )


@router.post('/auth/complete')
def post_auth_complete(tkn: token.Token = Depends(
    token.from_authotization_header_nondyn)):
    """
    Completes an authentication challenge for the owner of the token.
    """
    try:
        teamspeak.complete_authentication_challenge(
            teamspeak.new_connection(),
            tkn.owner,
        )
    except LookupError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail='Could not find corresponding teamspeak client')
    except me.DoesNotExist:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail='Could not find challenge for user')
