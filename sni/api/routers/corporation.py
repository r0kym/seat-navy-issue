"""
Corporation management paths
"""

from typing import Dict, Iterator, List

from fastapi import APIRouter, Depends
import pydantic as pdt

from sni.esi.token import tracking_status, TrackingStatus
from sni.uac.clearance import assert_has_clearance
from sni.uac.token import (
    from_authotization_header_nondyn,
    Token,
)
from sni.user.models import Corporation, User
from sni.user.user import ensure_corporation

from .user import GetUserShortOut

router = APIRouter()


class GetCorporationShortOut(pdt.BaseModel):
    """
    Short corporation description
    """
    corporation_id: int
    corporation_name: str

    @staticmethod
    def from_record(corporation: Corporation) -> 'GetCorporationShortOut':
        """
        Converts an instance of :class:`sni.user.models.Corporation` to
        :class:`sni.api.routers.corporation.GetCorporationShortOut`
        """
        return GetCorporationShortOut(
            corporation_id=corporation.corporation_id,
            corporation_name=corporation.corporation_name,
        )


class GetTrackingOut(pdt.BaseModel):
    """
    Represents a corporation tracking response.
    """
    invalid_refresh_token: List[GetUserShortOut] = []
    no_refresh_token: List[GetUserShortOut] = []
    valid_refresh_token: List[GetUserShortOut] = []

    @staticmethod
    def from_user_iterator(iterator: Iterator[User]) -> 'GetTrackingOut':
        """
        Creates a tracking response from a user iterator. See
        :meth:`sni.esi.token.tracking_status`
        """
        result = GetTrackingOut()
        ldict: Dict[int, List[GetUserShortOut]] = {
            TrackingStatus.HAS_NO_REFRESH_TOKEN: result.no_refresh_token,
            TrackingStatus.ONLY_HAS_INVALID_REFRESH_TOKEN:
            result.invalid_refresh_token,
            TrackingStatus.HAS_A_VALID_REFRESH_TOKEN:
            result.valid_refresh_token
        }
        for usr in iterator:
            status = tracking_status(usr)
            ldict[status].append(GetUserShortOut.from_record(usr))
        return result


@router.get(
    '/',
    response_model=List[GetCorporationShortOut],
    summary='Get the list of corporations',
)
def get_corporations(tkn: Token = Depends(from_authotization_header_nondyn), ):
    """
    Gets the list of corporations registered in this instance. Requires a
    clearance level of 0 or more.
    """
    assert_has_clearance(tkn.owner, 'sni.read_corporation')
    return [
        GetCorporationShortOut.from_record(corporation)
        for corporation in Corporation.objects()
    ]


@router.post(
    '/{corporation_id}',
    summary='Manually fetch a corporation from the ESI',
)
def post_corporation(
        corporation_id: int,
        tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Manually fetches a corporation from the ESI. Requires a clearance level of
    8 or more.
    """
    assert_has_clearance(tkn.owner, 'sni.fetch_corporation')
    ensure_corporation(corporation_id)


@router.get(
    '/{corporation_id}/tracking',
    response_model=GetTrackingOut,
    summary='Corporation tracking',
)
def get_corporation_tracking(
        corporation_id: int,
        tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Reports which member (of a given corporation) have a valid refresh token
    attacked to them, and which do not. Requires a clearance level of 1 and
    having authority over this corporation.
    """
    corporation: Corporation = Corporation.objects(
        corporation_id=corporation_id).get()
    assert_has_clearance(tkn.owner, 'sni.track_corporation', corporation.ceo)
    return GetTrackingOut.from_user_iterator(corporation.user_iterator())
