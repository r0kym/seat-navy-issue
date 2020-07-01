"""
Teamspeak related paths
"""

from datetime import datetime
import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
import mongoengine as me
import pydantic as pdt

import sni.teamspeak as teamspeak
import sni.conf as conf
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
    except (me.DoesNotExist, LookupError) as error:
        message = 'Could not complete authentication challenge for user ' \
            + tkn.owner.character_name
        if conf.get('general.debug'):
            message += ': ' + str(error)
        logging.error(message)
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=message)
