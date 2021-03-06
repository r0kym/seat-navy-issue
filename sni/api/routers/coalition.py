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

from sni.esi.scope import EsiScope
from sni.uac.clearance import assert_has_clearance
from sni.uac.token import (
    from_authotization_header_nondyn,
    Token,
)
from sni.user.models import Alliance, Coalition, Corporation

from .common import BSONObjectId
from .corporation import GetTrackingOut, GetCorporationShortOut

router = APIRouter()


class GetAllianceShortOut(pdt.BaseModel):
    """
    Short alliance description
    """

    alliance_id: int
    alliance_name: str

    @staticmethod
    def from_record(alliance: Alliance) -> "GetAllianceShortOut":
        """
        Converts an instance of :class:`sni.user.models.Alliance` to
        :class:`sni.api.routers.alliance.GetAllianceShortOut`
        """
        return GetAllianceShortOut(
            alliance_id=alliance.alliance_id,
            alliance_name=alliance.alliance_name,
        )


class GetCoalitionShortOut(pdt.BaseModel):
    """
    Model for an element of a `GET /coalition` response.
    """

    coalition_id: str
    coalition_name: str

    @staticmethod
    def from_record(coalition: Coalition) -> "GetCoalitionShortOut":
        """
        Converts a coalition database record to a short response.
        """
        return GetCoalitionShortOut(
            coalition_id=str(coalition.pk),
            coalition_name=coalition.coalition_name,
        )


class GetCoalitionOut(pdt.BaseModel):
    """
    Model for `GET /coalition/{coalition_id}` responses.
    """

    authorized_to_login: Optional[bool]
    coalition_id: str
    created_on: datetime
    mandatory_esi_scopes: List[EsiScope]
    member_alliances: List[GetAllianceShortOut]
    member_corporations: List[GetCorporationShortOut]
    coalition_name: str
    ticker: str
    updated_on: datetime

    @staticmethod
    def from_record(coalition: Coalition) -> "GetCoalitionOut":
        """
        Converts a coalition database record to a response.
        """
        return GetCoalitionOut(
            authorized_to_login=coalition.authorized_to_login,
            coalition_id=str(coalition.pk),
            created_on=coalition.created_on,
            mandatory_esi_scopes=coalition.mandatory_esi_scopes,
            member_alliances=[
                GetAllianceShortOut.from_record(member)
                for member in coalition.member_alliances
            ],
            member_corporations=[
                GetCorporationShortOut.from_record(member)
                for member in coalition.member_corporations
            ],
            coalition_name=coalition.coalition_name,
            ticker=coalition.ticker,
            updated_on=coalition.updated_on,
        )


class PostCoalitionIn(pdt.BaseModel):
    """
    Model for `POST /coalition` responses.
    """

    coalition_name: str
    ticker: str


class PutCoalitionIn(pdt.BaseModel):
    """
    Model for `PUT /coalition/{coalition_id}` responses.
    """

    add_member_alliances: Optional[List[int]] = None
    add_member_corporations: Optional[List[int]] = None
    authorized_to_login: Optional[bool] = None
    mandatory_esi_scopes: Optional[List[EsiScope]] = None
    member_alliances: Optional[List[int]] = None
    member_corporations: Optional[List[int]] = None
    remove_member_alliances: Optional[List[int]] = None
    remove_member_corporations: Optional[List[int]] = None
    ticker: Optional[str] = None


@router.delete(
    "/{coalition_id}", summary="Delete a coalition",
)
def delete_coalition(
    coalition_id: BSONObjectId,
    tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Deletes a coalition. Requires a clearance level of 9 or more.
    """
    assert_has_clearance(tkn.owner, "sni.delete_coalition")
    coalition: Coalition = Coalition.objects.get(pk=coalition_id)
    logging.debug(
        "Deleting coalition %s (%s)", coalition.coalition_name, coalition_id
    )
    coalition.delete()


@router.get(
    "",
    response_model=List[GetCoalitionShortOut],
    summary="List all coalition names",
)
def get_coalition(tkn: Token = Depends(from_authotization_header_nondyn)):
    """
    Lists all the coalition names. Requires a clearance level of 0 or more.
    """
    assert_has_clearance(tkn.owner, "sni.read_coalition")
    return [
        GetCoalitionShortOut.from_record(coalition)
        for coalition in Coalition.objects().order_by("coalition_name")
    ]


@router.get(
    "/{coalition_id}",
    response_model=GetCoalitionOut,
    summary="Get basic informations about a coalition",
)
def get_coalition_name(
    coalition_id: BSONObjectId,
    tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Returns details about a given coalition. Requires a clearance level of 0 or
    more.
    """
    assert_has_clearance(tkn.owner, "sni.read_coalition")
    return GetCoalitionOut.from_record(
        Coalition.objects(pk=coalition_id).get()
    )


@router.post(
    "",
    response_model=GetCoalitionOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a coalition",
)
def post_coalitions(
    data: PostCoalitionIn,
    tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Creates a coalition. Requires a clearance level of 9 or more.
    """
    assert_has_clearance(tkn.owner, "sni.create_coalition")
    coa = Coalition(
        coalition_name=data.coalition_name, ticker=data.ticker,
    ).save()
    logging.debug(
        "Created coalition %s (%s)", data.coalition_name, str(coa.pk)
    )
    return GetCoalitionOut.from_record(coa)


@router.put(
    "/{coalition_id}",
    response_model=GetCoalitionOut,
    summary="Update a coalition",
)
def put_coalition(
    coalition_id: BSONObjectId,
    data: PutCoalitionIn,
    tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Updates a coalition. All fields in the request body are optional. The
    `add_member_alliances` and `remove_member_alliances` fields can be used together, but the
    `member_alliances` cannot be used in conjunction with `add_member_alliances` and
    `remove_member_alliances`. Similarly for `add_member_corporations`,
    `remove_member_corporations`, and `member_corporations`. Requires a
    clearance level of 6 or more.
    """
    assert_has_clearance(tkn.owner, "sni.update_coalition")
    coalition: Coalition = Coalition.objects.get(pk=coalition_id)
    logging.debug(
        "Updating coalition %s (%s)", coalition.coalition_name, coalition_id
    )
    if data.add_member_alliances is not None:
        coalition.member_alliances += [
            Alliance.objects.get(alliance_id=member_id)
            for member_id in set(data.add_member_alliances)
        ]
    if data.add_member_corporations is not None:
        coalition.member_corporations += [
            Corporation.objects.get(corporation_id=member_id)
            for member_id in set(data.add_member_corporations)
        ]
    if data.authorized_to_login is not None:
        assert_has_clearance(tkn.owner, "sni.set_authorized_to_login")
        coalition.authorized_to_login = data.authorized_to_login
    if data.mandatory_esi_scopes is not None:
        coalition.mandatory_esi_scopes = data.mandatory_esi_scopes
    if data.member_alliances is not None:
        coalition.member_alliances = [
            Alliance.objects.get(alliance_id=member_id)
            for member_id in set(data.member_alliances)
        ]
    if data.member_corporations is not None:
        coalition.member_corporations = [
            Corporation.objects.get(corporation_id=member_id)
            for member_id in set(data.member_corporations)
        ]
    if data.remove_member_alliances is not None:
        coalition.member_alliances = [
            member
            for member in coalition.member_alliances
            if member.alliance_id not in data.remove_member_alliances
        ]
    if data.remove_member_corporations is not None:
        coalition.member_corporations = [
            member
            for member in coalition.member_corporations
            if member.corporation_id not in data.remove_member_corporations
        ]
    if data.ticker is not None:
        coalition.ticker = data.ticker
    coalition.member_corporations = list(set(coalition.member_corporations))
    coalition.member_alliances = list(set(coalition.member_alliances))
    coalition.save()
    return GetCoalitionOut.from_record(coalition)


@router.get(
    "/{coalition_id}/tracking",
    response_model=GetTrackingOut,
    summary="Coalition tracking",
)
def get_coalition_tracking(
    coalition_id: BSONObjectId,
    tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Reports which member (of a given coalition) have a valid refresh token
    attacked to them, and which do not. Requires a clearance level of 5 or
    more.
    """
    coalition: Coalition = Coalition.objects(pk=coalition_id).get()
    assert_has_clearance(tkn.owner, "sni.track_coalition")
    return GetTrackingOut.from_user_iterator(coalition.user_iterator())
