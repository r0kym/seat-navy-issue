"""
Alliance management paths
"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends
import pydantic as pdt

from sni.esi.scope import EsiScope
from sni.scheduler import scheduler
from sni.uac.clearance import assert_has_clearance
from sni.uac.token import (
    from_authotization_header_nondyn,
    Token,
)
from sni.user.models import Alliance
from sni.user.user import ensure_alliance
from sni.user.jobs import ensure_alliance_members

from .corporation import (
    GetAllianceShortOut,
    GetTrackingOut,
    GetCorporationShortOut,
)
from .user import GetUserShortOut

router = APIRouter()


class GetAllianceOut(pdt.BaseModel):
    """
    Get an alliance data
    """

    alliance_id: int
    alliance_name: str
    authorized_to_login: Optional[bool]
    ceo: GetUserShortOut
    cumulated_mandatory_esi_scopes: List[EsiScope]
    executor_corporation: GetCorporationShortOut
    mandatory_esi_scopes: List[EsiScope]
    ticker: str
    updated_on: datetime

    @staticmethod
    def from_record(alliance: Alliance) -> "GetAllianceOut":
        """
        Converts an instance of :class:`sni.user.models.Alliance` to
        :class:`sni.api.routers.alliance.GetAllianceOut`
        """
        return GetAllianceOut(
            alliance_id=alliance.alliance_id,
            alliance_name=alliance.alliance_name,
            authorized_to_login=alliance.authorized_to_login,
            ceo=GetUserShortOut.from_record(alliance.ceo),
            executor_corporation=GetCorporationShortOut.from_record(
                alliance.executor
            ),
            mandatory_esi_scopes=alliance.mandatory_esi_scopes,
            cumulated_mandatory_esi_scopes=list(
                alliance.cumulated_mandatory_esi_scopes()
            ),
            ticker=alliance.ticker,
            updated_on=alliance.updated_on,
        )


class PutAllianceIn(pdt.BaseModel):
    """
    Model for ``PUT /alliance/{alliance_id}`` requests
    """

    authorized_to_login: Optional[bool]
    mandatory_esi_scopes: Optional[List[EsiScope]]


@router.get(
    "",
    response_model=List[GetAllianceShortOut],
    summary="Get the list of alliances",
)
def get_alliances(tkn: Token = Depends(from_authotization_header_nondyn),):
    """
    Gets the list of alliances registered in this instance. Requires a
    clearance level of 0 or more.
    """
    assert_has_clearance(tkn.owner, "sni.read_alliance")
    return [
        GetAllianceShortOut.from_record(alliance)
        for alliance in Alliance.objects().order_by("alliance_name")
    ]


@router.get(
    "/{alliance_id}", summary="Get data about an alliance",
)
def get_alliance(
    alliance_id: int, tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Gets data about an alliance
    """
    assert_has_clearance(tkn.owner, "sni.read_alliance")
    alliance = Alliance.objects(alliance_id=alliance_id).get()
    return GetAllianceOut.from_record(alliance)


@router.post(
    "/{alliance_id}",
    response_model=GetAllianceOut,
    summary="Manually fetch an alliance from the ESI",
)
def post_alliance(
    alliance_id: int, tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Manually fetches an alliance from the ESI. Requires a clearance level of
    8 or more.
    """
    assert_has_clearance(tkn.owner, "sni.fetch_alliance")
    alliance = ensure_alliance(alliance_id)
    scheduler.add_job(ensure_alliance_members, args=(alliance,))
    return GetAllianceOut.from_record(alliance)


@router.put(
    "/{alliance_id}",
    response_model=GetAllianceOut,
    summary="Modify an alliance registered on SNI",
)
def put_alliance(
    alliance_id: int,
    data: PutAllianceIn,
    tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Modify an alliance registered on SNI. Note that it does not modify it on an
    ESI level. Requires a clearance level of 4 or more.
    """
    alliance: Alliance = Alliance.objects(alliance_id=alliance_id).get()
    assert_has_clearance(tkn.owner, "sni.update_alliance", alliance.ceo)
    alliance.authorized_to_login = data.authorized_to_login
    if data.mandatory_esi_scopes is not None:
        alliance.mandatory_esi_scopes = data.mandatory_esi_scopes
    alliance.save()
    return GetAllianceOut.from_record(alliance)


@router.get(
    "/{alliance_id}/tracking",
    response_model=GetTrackingOut,
    summary="Alliance tracking",
)
def get_alliance_tracking(
    alliance_id: int, tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Reports which member (of a given alliance) have a valid refresh token
    attacked to them, and which do not. Requires a clearance level of 3 and
    having authority over this alliance.
    """
    alliance: Alliance = Alliance.objects(alliance_id=alliance_id).get()
    assert_has_clearance(tkn.owner, "sni.track_alliance", alliance.ceo)
    return GetTrackingOut.from_user_iterator(alliance.user_iterator())
