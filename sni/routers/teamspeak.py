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
import ts3
import ts3.query

import sni.teamspeak.teamspeak as teamspeak
import sni.time as time
import sni.uac.clearance as clearance
import sni.uac.token as token
import sni.uac.user as user

router = APIRouter()


class GetGroupMappingOut(pdt.BaseModel):
    """
    Model for an element of `GET /teamspeak/group` responses.
    """
    sni_group_name: str
    ts_group_id: str
    ts_group_name: str


class GetUserOut(pdt.BaseModel):
    """
    Model for `GET /teamspeak/user/{name}` responses.
    """
    character_name: str
    client_database_id: int
    created_on: datetime


class PostAuthStartOut(pdt.BaseModel):
    """
    Model for `POST /teamspeak/auth/start` responses.
    """
    expiration_datetime: datetime
    challenge_nickname: str
    user: str


def teamspeak_group_mapping_record_to_response(
        connection: ts3.query.TS3Connection,
        mapping: teamspeak.TeamspeakGroupMapping) -> GetGroupMappingOut:
    """
    Converts a :class:`sni.teamspeak.TeamspeakGroupMapping` to a :class:`sni.routers.teamspeak.GetGroupMappingOut`.
    """
    ts_group_name = teamspeak.find_group(connection,
                                         group_id=mapping.teamspeak_group_id)
    return GetGroupMappingOut(
        sni_group_name=mapping.sni_group.name,
        ts_group_id=mapping.teamspeak_group_id,
        ts_group_name=ts_group_name,
    )


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


@router.get(
    '/group',
    response_model=List[GetGroupMappingOut],
    summary='Get all group mappings',
)
def get_group(tkn: token.Token = Depends(
    token.from_authotization_header_nondyn)):
    """
    Gets informations about all Teamspeak group mappings. Requires a clearance
    level of 0 or more.
    """
    clearance.assert_has_clearance(tkn.owner,
                                   'sni.teamspeak.read_group_mapping')
    connection = teamspeak.new_connection()
    return [
        teamspeak_group_mapping_record_to_response(connection, mapping)
        for mapping in teamspeak.TeamspeakGroupMapping.objects
    ]


@router.delete(
    '/group/{sni_group_name}/{ts_group_name}',
    summary='Deletes a Teamseak group mapping',
)
def delete_group_mapping(sni_group_name: str,
                         ts_group_name: str,
                         tkn: token.Token = Depends(
                             token.from_authotization_header_nondyn)):
    """
    Deletes a Teamspeak group mapping. Does not immediately update the
    teamspeak users group memberships. Requires a clearance level of 9 or more.
    """
    clearance.assert_has_clearance(tkn.owner,
                                   'sni.teamspeak.delete_group_mapping')
    sni_group = user.Group.objects(name=sni_group_name).get()
    teamspeak_group_id = teamspeak.find_group(teamspeak.new_connection(),
                                              name=ts_group_name)
    teamspeak.TeamspeakGroupMapping.objects(
        sni_group=sni_group,
        teamspeak_group_id=teamspeak_group_id,
    ).delete()


@router.post(
    '/group/{sni_group_name}/{ts_group_name}',
    status_code=status.HTTP_201_CREATED,
    summary='Maps a SNI group to a Teamspeak group',
)
def post_group_mapping(sni_group_name: str,
                       ts_group_name: str,
                       tkn: token.Token = Depends(
                           token.from_authotization_header_nondyn)):
    """
    Maps a SNI group to a Teamspeak group. This mean that users belonging to
    that SNI group will be affected to that Teamspeak group, if they are
    registered on Teamspeak. Requires a clearance level of 9 or more.
    """
    clearance.assert_has_clearance(tkn.owner,
                                   'sni.teamspeak.create_group_mapping')
    sni_group = user.Group.objects(name=sni_group_name).get()
    teamspeak_group_id = teamspeak.find_group(teamspeak.new_connection(),
                                              name=ts_group_name)
    teamspeak.TeamspeakGroupMapping.objects(
        sni_group=sni_group,
        teamspeak_group_id=teamspeak_group_id,
    ).modify(
        set__sni_group=sni_group,
        set__teamspeak_group_id=teamspeak_group_id,
        upsert=True,
    )
