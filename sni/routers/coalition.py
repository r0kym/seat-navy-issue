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

import sni.time as time
import sni.uac.clearance as clearance
import sni.uac.token as token
import sni.uac.user as user

router = APIRouter()


class GetCoalitionOut(pdt.BaseModel):
    """
    Model for ``GET /coalition/{name}`` responses.
    """
    created_on: datetime
    members: List[str]
    name: str
    ticker: str
    updated_on: datetime


class PostCoalitionIn(pdt.BaseModel):
    """
    Model for ``POST /coalition`` responses.
    """
    name: str
    ticker: str


class PutCoalitionIn(pdt.BaseModel):
    """
    Model for ``POST /coalition`` responses.
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
        created_on=coa.created_on,
        members=[member.alliance_name for member in coa.members],
        name=coa.name,
        ticker=coa.ticker,
        updated_on=coa.updated_on,
    )


@router.delete('/{coalition_name}')
def delete_coalition(
        coalition_name: str,
        tkn: token.Token = Depends(token.from_authotization_header_nondyn),
):
    """
    Deletes a coalition.
    """
    clearance.assert_has_clearance(tkn.owner, 'sni.write_coalition')
    coa: user.Coalition = user.Coalition.objects.get(name=coalition_name)
    logging.debug('Deleting coalition %s', coalition_name)
    coa.delete()


@router.get('/', response_model=List[str])
def get_coalition(tkn: token.Token = Depends(
    token.from_authotization_header_nondyn)):
    """
    Lists all the coalition names.
    """
    clearance.assert_has_clearance(tkn.owner, 'sni.read_coalition')
    return [coalition.name for coalition in user.Coalition.objects()]


@router.get('/{coalition_name}', response_model=GetCoalitionOut)
def get_coalition_name(
        coalition_name: str,
        tkn: token.Token = Depends(token.from_authotization_header_nondyn),
):
    """
    Returns details about a given coalition.
    """
    clearance.assert_has_clearance(tkn.owner, 'sni.read_coalition')
    return coalition_record_to_response(
        user.Coalition.objects(name=coalition_name).get())


@router.post(
    '/',
    response_model=GetCoalitionOut,
    status_code=status.HTTP_201_CREATED,
)
def post_coalitions(
        data: PostCoalitionIn,
        tkn: token.Token = Depends(token.from_authotization_header_nondyn),
):
    """
    Creates a coalition.
    """
    clearance.assert_has_clearance(tkn.owner, 'sni.write_coalition')
    coa = user.Coalition(
        name=data.name,
        ticker=data.ticker,
    ).save()
    logging.debug('Created coalition %s', data.name)
    return coalition_record_to_response(coa)


@router.put('/{coalition_name}', response_model=GetCoalitionOut)
def put_coalition(
        coalition_name: str,
        data: PutCoalitionIn,
        tkn: token.Token = Depends(token.from_authotization_header_nondyn),
):
    """
    Updates a coalition. All fields in the request body are optional. The
    ``add_members`` and ``remove_members`` fields can be used together, but the
    ``members`` cannot be used in conjunction with ``add_members`` and
    ``remove_members``.
    """
    clearance.assert_has_clearance(tkn.owner, 'sni.write_coalition')
    coa: user.Coalition = user.Coalition.objects.get(name=coalition_name)
    logging.debug('Updating coalition %s', coalition_name)
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
    coa.updated_on = time.now()
    coa.save()
    return coalition_record_to_response(coa)
