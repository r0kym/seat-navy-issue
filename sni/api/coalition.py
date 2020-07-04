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

import sni.uac.clearance as clearance
import sni.uac.token as token
import sni.user.user as user

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
    coalition_id: str
    created_on: datetime
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
    add_members: Optional[List[str]] = None
    members: Optional[List[str]] = None
    remove_members: Optional[List[str]] = None
    ticker: Optional[str] = None


def coalition_record_to_response(coa: user.Coalition) -> GetCoalitionOut:
    """
    Converts a coalition database record to a response.
    """
    return GetCoalitionOut(
        coalition_id=str(coa.pk),
        created_on=coa.created_on,
        members=[member.alliance_id for member in coa.members],
        coalition_name=coa.name,
        ticker=coa.ticker,
        updated_on=coa.updated_on,
    )


@router.delete(
    '/{coalition_id}',
    summary='Delete a coalition',
)
def delete_coalition(
        coalition_id: str,
        tkn: token.Token = Depends(token.from_authotization_header_nondyn),
):
    """
    Deletes a coalition. Requires a clearance level of 9 or more.
    """
    clearance.assert_has_clearance(tkn.owner, 'sni.delete_coalition')
    coa: user.Coalition = user.Coalition.objects.get(pk=coalition_id)
    logging.debug('Deleting coalition %s (%s)', coa.name, coalition_id)
    coa.delete()


@router.get(
    '',
    response_model=List[GetCoalitionShortOut],
    summary='List all coalition names',
)
def get_coalition(tkn: token.Token = Depends(
    token.from_authotization_header_nondyn)):
    """
    Lists all the coalition names. Requires a clearance level of 0 or more.
    """
    clearance.assert_has_clearance(tkn.owner, 'sni.read_coalition')
    return [
        GetCoalitionShortOut(coalition_id=str(coa.pk), coalition_name=coa.name)
        for coa in user.Coalition.objects()
    ]


@router.get(
    '/{coalition_id}',
    response_model=GetCoalitionOut,
    summary='Get basic informations about a coalition',
)
def get_coalition_name(
        coalition_id: str,
        tkn: token.Token = Depends(token.from_authotization_header_nondyn),
):
    """
    Returns details about a given coalition. Requires a clearance level of 0 or
    more.
    """
    clearance.assert_has_clearance(tkn.owner, 'sni.read_coalition')
    return coalition_record_to_response(
        user.Coalition.objects(pk=coalition_id).get())


@router.post(
    '',
    response_model=GetCoalitionOut,
    status_code=status.HTTP_201_CREATED,
    summary='Create a coalition',
)
def post_coalitions(
        data: PostCoalitionIn,
        tkn: token.Token = Depends(token.from_authotization_header_nondyn),
):
    """
    Creates a coalition. Requires a clearance level of 9 or more.
    """
    clearance.assert_has_clearance(tkn.owner, 'sni.create_coalition')
    coa = user.Coalition(
        name=data.coalition_name,
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
        tkn: token.Token = Depends(token.from_authotization_header_nondyn),
):
    """
    Updates a coalition. All fields in the request body are optional. The
    `add_members` and `remove_members` fields can be used together, but the
    `members` cannot be used in conjunction with `add_members` and
    `remove_members`. Requires a clearance level of 9 or more.
    """
    clearance.assert_has_clearance(tkn.owner, 'sni.update_coalition')
    coa: user.Coalition = user.Coalition.objects.get(pk=coalition_id)
    logging.debug('Updating coalition %s (%s)', coa.name, coalition_id)
    if data.add_members is not None:
        coa.members += [
            user.Alliance.objects.get(alliance_name=member_name)
            for member_name in set(data.add_members)
        ]
    if data.members is not None:
        coa.members = [
            user.Alliance.objects.get(alliance_name=member_name)
            for member_name in set(data.members)
        ]
    if data.remove_members is not None:
        coa.members = [
            member for member in coa.members
            if member.alliance_name not in data.remove_members
        ]
    if data.ticker is not None:
        coa.ticker = data.ticker
    coa.save()
    return coalition_record_to_response(coa)
