"""
Group management paths
"""

from datetime import datetime
import logging
from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    status,
)
import pydantic as pdt

import sni.time as time
import sni.uac.clearance as clearance
import sni.uac.group as group
import sni.uac.token as token
import sni.uac.user as user

router = APIRouter()


class GetGroupOut(pdt.BaseModel):
    """
    Model for `GET /group/{name}` responses.
    """
    created_on: datetime
    description: str
    members: List[str]
    name: str
    owner: str
    updated_on: datetime


class PostGroupIn(pdt.BaseModel):
    """
    Model for `POST /group` responses.
    """
    name: str
    description: str = ''


class PutGroupIn(pdt.BaseModel):
    """
    Model for `POST /group` responses.
    """
    add_members: Optional[List[str]] = None
    description: Optional[str] = None
    members: Optional[List[str]] = None
    owner: Optional[str] = None
    remove_members: Optional[List[str]] = None


def group_record_to_response(grp: group.Group) -> GetGroupOut:
    """
    Converts a group database record to a response.
    """
    return GetGroupOut(
        created_on=grp.created_on,
        description=grp.description,
        members=[member.character_name for member in grp.members],
        name=grp.name,
        owner=grp.owner.character_name,
        updated_on=grp.updated_on,
    )


@router.delete(
    '/{group_name}',
    summary='Delete a group',
)
def delete_group(
        group_name: str,
        tkn: token.Token = Depends(token.from_authotization_header_nondyn),
):
    """
    Deletes a group. Requires a clearance level of 9 or more.
    """
    clearance.assert_has_clearance(tkn.owner, 'sni.delete_group')
    grp: group.Group = group.Group.objects.get(name=group_name)
    logging.debug('Deleting group %s', group_name)
    grp.delete()


@router.get(
    '/',
    response_model=List[str],
    summary='List all group names',
)
def get_group(
        tkn: token.Token = Depends(token.from_authotization_header_nondyn), ):
    """
    Lists all the group names. Requires a clearance level of 0 or more.
    """
    clearance.assert_has_clearance(tkn.owner, 'sni.read_group')
    return [grp.name for grp in group.Group.objects()]


@router.get(
    '/{group_name}',
    response_model=GetGroupOut,
    summary='Get basic informations about a group',
)
def get_group_name(
        group_name: str,
        tkn: token.Token = Depends(token.from_authotization_header_nondyn),
):
    """
    Returns details about a given group. Requires a clearance level of 0 or
    more.
    """
    clearance.assert_has_clearance(tkn.owner, 'sni.read_group')
    return group_record_to_response(group.Group.objects(name=group_name).get())


@router.post(
    '/',
    response_model=GetGroupOut,
    status_code=status.HTTP_201_CREATED,
    summary='Create a group',
)
def post_groups(
        data: PostGroupIn,
        tkn: token.Token = Depends(token.from_authotization_header_nondyn),
):
    """
    Creates a group. Requires a clearance level of 9 or more.
    """
    clearance.assert_has_clearance(tkn.owner, 'sni.create_group')
    grp = group.Group(
        description=data.description,
        members=[tkn.owner],
        name=data.name,
        owner=tkn.owner,
    ).save()
    logging.debug('Created group %s owned by %s', data.name,
                  tkn.owner.character_name)
    return group_record_to_response(grp)


@router.put(
    '/{group_name}',
    response_model=GetGroupOut,
    summary='Update a group',
)
def put_group(
        group_name: str,
        data: PutGroupIn,
        tkn: token.Token = Depends(token.from_authotization_header_nondyn),
):
    """
    Updates a group. All fields in the request body are optional. The
    `add_members` and `remove_members` fields can be used together, but the
    `members` cannot be used in conjunction with `add_members` and
    `remove_members`. Requires a clearance level of 9 or more of for the user
    to be the owner of the group.
    """
    grp: group.Group = group.Group.objects.get(name=group_name)
    if not (tkn.owner == grp.owner
            or clearance.has_clearance(tkn.owner, 'sni.update_group')):
        raise PermissionError
    logging.debug('Updating group %s', group_name)
    if data.add_members is not None:
        grp.members += [
            user.User.objects.get(character_name=member_name)
            for member_name in set(data.add_members)
        ]
    if data.description is not None:
        grp.description = data.description
    if data.members is not None:
        grp.members = [
            user.User.objects.get(character_name=member_name)
            for member_name in set(data.members)
        ]
    if data.owner is not None:
        grp.owner = user.User.objects.get(character_name=data.owner)
    if data.remove_members is not None:
        grp.members = [
            member for member in grp.members
            if member.character_name not in data.remove_members
        ]
    grp.members = list(set(grp.members + [grp.owner]))
    grp.updated_on = time.now()
    grp.save()
    return group_record_to_response(grp)
