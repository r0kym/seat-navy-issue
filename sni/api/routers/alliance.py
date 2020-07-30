"""
Alliance management paths
"""

from typing import List

from fastapi import APIRouter, Depends
import pydantic as pdt

from sni.scheduler import scheduler
from sni.uac.clearance import assert_has_clearance
from sni.uac.token import (
    from_authotization_header_nondyn,
    Token,
)
from sni.user.models import Alliance
from sni.user.user import ensure_alliance
from sni.user.jobs import ensure_alliance_members

from .corporation import GetTrackingOut

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


@router.post(
    "/{alliance_id}", summary="Manually fetch an alliance from the ESI",
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
