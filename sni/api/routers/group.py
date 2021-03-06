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

from sni.user.models import Group, User

from sni.uac.clearance import assert_has_clearance, has_clearance
from sni.uac.token import (
    from_authotization_header_nondyn,
    Token,
)

from .user import GetUserShortOut
from .common import BSONObjectId

router = APIRouter()


class GetGroupShortOut(pdt.BaseModel):
    """
    Model for an element of `GET /group` responses
    """

    group_id: str
    group_name: str


class GetGroupOut(pdt.BaseModel):
    """
    Model for `GET /group/{group_id}` responses.
    """

    authorized_to_login: Optional[bool]
    created_on: datetime
    description: str
    group_id: str
    group_name: str
    is_autogroup: bool
    members: List[GetUserShortOut]
    owner: Optional[GetUserShortOut]
    updated_on: datetime

    @staticmethod
    def from_record(grp: Group) -> "GetGroupOut":
        """
        Converts a group database record to a response.
        """
        return GetGroupOut(
            authorized_to_login=grp.authorized_to_login,
            created_on=grp.created_on,
            description=grp.description,
            group_id=str(grp.pk),
            group_name=grp.group_name,
            is_autogroup=grp.is_autogroup,
            members=[
                GetUserShortOut.from_record(member) for member in grp.members
            ],
            owner=GetUserShortOut.from_record(grp.owner)
            if grp.owner is not None
            else None,
            updated_on=grp.updated_on,
        )


class PostGroupIn(pdt.BaseModel):
    """
    Model for `POST /group` responses.
    """

    description: str = ""
    group_name: str


class PutGroupIn(pdt.BaseModel):
    """
    Model for `POST /group` responses.
    """

    add_members: Optional[List[str]] = None
    authorized_to_login: Optional[bool]
    description: Optional[str] = None
    members: Optional[List[str]] = None
    owner: Optional[str] = None
    remove_members: Optional[List[str]] = None


@router.delete(
    "/{group_id}", summary="Delete a group",
)
def delete_group(
    group_id: BSONObjectId,
    tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Deletes a group. Requires a clearance level of 9 or more.
    """
    assert_has_clearance(tkn.owner, "sni.delete_group")
    grp: Group = Group.objects.get(pk=group_id)
    logging.debug("Deleting group %s (%s)", grp.group_name, group_id)
    grp.delete()


@router.get(
    "", response_model=List[GetGroupShortOut], summary="List all group names",
)
def get_group(tkn: Token = Depends(from_authotization_header_nondyn),):
    """
    Lists all the group names. Requires a clearance level of 0 or more.
    """
    assert_has_clearance(tkn.owner, "sni.read_group")
    return [
        GetGroupShortOut(group_id=str(grp.pk), group_name=grp.group_name)
        for grp in Group.objects().order_by("group_name")
    ]


@router.get(
    "/{group_id}",
    response_model=GetGroupOut,
    summary="Get basic informations about a group",
)
def get_group_name(
    group_id: BSONObjectId,
    tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Returns details about a given group. Requires a clearance level of 0 or
    more.
    """
    assert_has_clearance(tkn.owner, "sni.read_group")
    return GetGroupOut.from_record(Group.objects(pk=group_id).get())


@router.post(
    "",
    response_model=GetGroupOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a group",
)
def post_groups(
    data: PostGroupIn, tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Creates a group. Requires a clearance level of 9 or more.
    """
    assert_has_clearance(tkn.owner, "sni.create_group")
    grp = Group(
        description=data.description,
        members=[tkn.owner],
        group_name=data.group_name,
        owner=tkn.owner,
    ).save()
    logging.debug(
        "Created group %s (%s) owned by %s",
        data.group_name,
        str(grp.pk),
        tkn.owner.character_name,
    )
    return GetGroupOut.from_record(grp)


@router.put(
    "/{group_id}", response_model=GetGroupOut, summary="Update a group",
)
def put_group(
    group_id: BSONObjectId,
    data: PutGroupIn,
    tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Updates a group. All fields in the request body are optional. The
    `add_members` and `remove_members` fields can be used together, but the
    `members` cannot be used in conjunction with `add_members` and
    `remove_members`. Requires a clearance level of 9 or more of for the user
    to be the owner of the group.
    """
    grp: Group = Group.objects.get(pk=group_id)
    if not (
        tkn.owner == grp.owner or has_clearance(tkn.owner, "sni.update_group")
    ):
        raise PermissionError
    logging.debug("Updating group %s (%s)", grp.group_name, group_id)
    if data.add_members is not None:
        grp.members += [
            User.objects.get(character_name=member_name)
            for member_name in set(data.add_members)
        ]
    if data.authorized_to_login is not None:
        assert_has_clearance(tkn.owner, "sni.set_authorized_to_login")
        grp.authorized_to_login = data.authorized_to_login
    if data.description is not None:
        grp.description = data.description
    if data.members is not None:
        grp.members = [
            User.objects.get(character_name=member_name)
            for member_name in set(data.members)
        ]
    if data.owner is not None:
        grp.owner = User.objects.get(character_name=data.owner)
    if data.remove_members is not None:
        grp.members = [
            member
            for member in grp.members
            if member.character_name not in data.remove_members
        ]
    grp.members = list(set(grp.members + [grp.owner]))
    grp.save()
    return GetGroupOut.from_record(grp)
