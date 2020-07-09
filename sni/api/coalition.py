"""
Coalition management paths

Todo:
    Code is too similar to :mod:`sni.routers.group`
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

from sni.uac.clearance import assert_has_clearance
from sni.uac.token import (
    from_authotization_header_nondyn,
    Token,
)
from sni.user.models import Alliance, Coalition

router = APIRouter()


class GetCoalitionShortOut(pdt.BaseModel):
    """
    Model for an element of a `GET /coalition` response.
    """
    coalition_id: str
    coalition_name: str


class GetCoalitionOut(pdt.BaseModel):
    """
    Model for `GET /coalition/{coalition_id}` responses.
    """
    authorized_to_login: Optional[bool]
    coalition_id: str
    created_on: datetime
    mandatory_esi_scopes: List[str]
    members: List[str]
    coalition_name: str
    ticker: str
    updated_on: datetime


class PostCoalitionIn(pdt.BaseModel):
    """
    Model for `POST /coalition` responses.
    """
    coalition_name: str
    ticker: str


class PutCoalitionIn(pdt.BaseModel):
    """
    Model for `POST /coalition` responses.
    """
    add_members: Optional[List[int]] = None
    authorized_to_login: Optional[bool]
    mandatory_esi_scopes: Optional[List[str]]
    members: Optional[List[int]] = None
    remove_members: Optional[List[int]] = None
    ticker: Optional[str] = None


def coalition_record_to_response(coalition: Coalition) -> GetCoalitionOut:
    """
    Converts a coalition database record to a response.
    """
    return GetCoalitionOut(
        authorized_to_login=coalition.authorized_to_login,
        coalition_id=str(coalition.pk),
        created_on=coalition.created_on,
        mandatory_esi_scopes=coalition.mandatory_esi_scopes,
        members=[member.alliance_id for member in coalition.members],
        coalition_name=coalition.coalition_name,
        ticker=coalition.ticker,
        updated_on=coalition.updated_on,
    )


@router.delete(
    '/{coalition_id}',
    summary='Delete a coalition',
)
def delete_coalition(
        coalition_id: str,
        tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Deletes a coalition. Requires a clearance level of 9 or more.
    """
    assert_has_clearance(tkn.owner, 'sni.delete_coalition')
    coalition: Coalition = Coalition.objects.get(pk=coalition_id)
    logging.debug('Deleting coalition %s (%s)', coalition.coalition_name,
                  coalition_id)
    coalition.delete()


@router.get(
    '',
    response_model=List[GetCoalitionShortOut],
    summary='List all coalition names',
)
def get_coalition(tkn: Token = Depends(from_authotization_header_nondyn)):
    """
    Lists all the coalition names. Requires a clearance level of 0 or more.
    """
    assert_has_clearance(tkn.owner, 'sni.read_coalition')
    return [
        GetCoalitionShortOut(coalition_id=str(coalition.pk),
                             coalition_name=coalition.coalition_name)
        for coalition in Coalition.objects()
    ]


@router.get(
    '/{coalition_id}',
    response_model=GetCoalitionOut,
    summary='Get basic informations about a coalition',
)
def get_coalition_name(
        coalition_id: str,
        tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Returns details about a given coalition. Requires a clearance level of 0 or
    more.
    """
    assert_has_clearance(tkn.owner, 'sni.read_coalition')
    return coalition_record_to_response(
        Coalition.objects(pk=coalition_id).get())


@router.post(
    '',
    response_model=GetCoalitionOut,
    status_code=status.HTTP_201_CREATED,
    summary='Create a coalition',
)
def post_coalitions(
        data: PostCoalitionIn,
        tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Creates a coalition. Requires a clearance level of 9 or more.
    """
    assert_has_clearance(tkn.owner, 'sni.create_coalition')
    coa = Coalition(
        coalition_name=data.coalition_name,
        ticker=data.ticker,
    ).save()
    logging.debug('Created coalition %s (%s)', data.coalition_name,
                  str(coa.pk))
    return coalition_record_to_response(coa)


@router.put(
    '/{coalition_id}',
    response_model=GetCoalitionOut,
    summary='Update a coalition',
)
def put_coalition(
        coalition_id: str,
        data: PutCoalitionIn,
        tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Updates a coalition. All fields in the request body are optional. The
    `add_members` and `remove_members` fields can be used together, but the
    `members` cannot be used in conjunction with `add_members` and
    `remove_members`. Requires a clearance level of 9 or more.
    """
    assert_has_clearance(tkn.owner, 'sni.update_coalition')
    coalition: Coalition = Coalition.objects.get(pk=coalition_id)
    logging.debug('Updating coalition %s (%s)', coalition.coalition_name,
                  coalition_id)
    if data.add_members is not None:
        coalition.members += [
            Alliance.objects.get(alliance_id=member_id)
            for member_id in set(data.add_members)
        ]
    if data.authorized_to_login is not None:
        assert_has_clearance(tkn.owner, 'sni.set_authorized_to_login')
        coalition.authorized_to_login = data.authorized_to_login
    if data.mandatory_esi_scopes is not None:
        coalition.mandatory_esi_scopes = data.mandatory_esi_scopes
    if data.members is not None:
        coalition.members = [
            Alliance.objects.get(alliance_id=member_id)
            for member_id in set(data.members)
        ]
    if data.remove_members is not None:
        coalition.members = [
            member for member in coalition.members
            if member.alliance_id not in data.remove_members
        ]
    if data.ticker is not None:
        coalition.ticker = data.ticker
    coalition.save()
    return coalition_record_to_response(coalition)
