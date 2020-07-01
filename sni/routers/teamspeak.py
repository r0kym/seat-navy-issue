"""
Teamspeak related paths
"""

from datetime import datetime
from typing import List

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
import sni.uac.clearance as clearance
import sni.uac.token as token
import sni.uac.user as user

router = APIRouter()


class PostAuthStartOut(pdt.BaseModel):
    """
    Model for `POST /teamspeak/auth/start` responses.
    """
    expiration_datetime: datetime
    challenge_nickname: str
    user: str


class GetUserOut(pdt.BaseModel):
    """
    Model for `GET /teamspeak/user/{name}` responses.
    """
    character_name: str
    client_database_id: int
    created_on: datetime


def teamspeak_user_record_to_response(
        usr: teamspeak.TeamspeakUser) -> GetUserOut:
    """
    Converts a :class:`sni.teamspeak.TeamspeakUser` to a :class:`sni.routers.teamspeak.GetUserOut`.
    """
    return GetUserOut(
        character_name=usr.user.character_name,
        client_database_id=usr.teamspeak_id,
        created_on=usr.created_on,
    )


@router.get(
    '/user',
    response_model=List[str],
    summary='Lists all EVE characters registered on Teamspeak',
)
def get_teamspeak_users(tkn: token.Token = Depends(
    token.from_authotization_header_nondyn)):
    """
    Lists all EVE characters registered on Teamspeak. Requires a clearance
    level of 0 or more.
    """
    clearance.assert_has_clearance(tkn.owner, 'sni.teamspeak.read_user')
    return [
        tsusr.user.character_name
        for tsusr in teamspeak.TeamspeakUser.objects()
    ]


@router.get(
    '/user/{name}',
    response_model=GetUserOut,
    summary='Get basic teamspeak informations about a registered EVE character',
)
def get_teamspeak_user(name: str,
                       tkn: token.Token = Depends(
                           token.from_authotization_header_nondyn)):
    """
    Get basic teamspeak informations about a registered EVE character. In other
    words, the `name` parameter is expected to be an EVE character name.
    Requires a clearance level of 0 or more.
    """
    clearance.assert_has_clearance(tkn.owner, 'sni.teamspeak.read_user')
    usr = user.User.objects(character_name=name).get()
    tsusr = teamspeak.TeamspeakUser.objects(user=usr).get()
    return teamspeak_user_record_to_response(tsusr)


@router.post(
    '/auth/start',
    response_model=PostAuthStartOut,
    summary='Starts a teamspeak authentication challenge',
)
def port_auth_start(tkn: token.Token = Depends(
    token.from_authotization_header_nondyn)):
    """
    Starts a new authentication challenge for the owner of the token. A random
    nickname is returned (see `PostAuthStartOut` for more details), and the
    user has 1 minute to update its teamspeak nickname to it, and then call
    `POST /teamspeak/auth/complete`.
    """
    clearance.assert_has_clearance(tkn.owner, 'sni.teamspeak.auth')
    return PostAuthStartOut(
        expiration_datetime=time.now_plus(seconds=60),
        challenge_nickname=teamspeak.new_authentication_challenge(tkn.owner),
        user=tkn.owner.character_name,
    )


@router.post(
    '/auth/complete',
    status_code=status.HTTP_201_CREATED,
    summary='Completes a teamspeak authentication challenge',
)
def post_auth_complete(tkn: token.Token = Depends(
    token.from_authotization_header_nondyn)):
    """
    Completes an authentication challenge for the owner of the token. See the
    `POST /teamspeak/auth/start` documentation.
    """
    clearance.assert_has_clearance(tkn.owner, 'sni.teamspeak.auth')
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
