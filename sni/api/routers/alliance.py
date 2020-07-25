"""
Alliance management paths
"""

from fastapi import APIRouter, Depends

from sni.uac.clearance import assert_has_clearance
from sni.uac.token import (
    from_authotization_header_nondyn,
    Token,
)
from sni.user.models import Alliance
from sni.user.user import ensure_alliance

from .corporation import GetTrackingOut

router = APIRouter()


@router.post(
    '/{alliance_id}',
    summary='Manually fetch an alliance from the ESI',
)
def post_alliance(
        alliance_id: int,
        tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Manually fetches an alliance from the ESI. Requires a clearance level of
    8 or more.
    """
    assert_has_clearance(tkn.owner, 'sni.fetch_alliance')
    ensure_alliance(alliance_id)


@router.get(
    '/{alliance_id}/tracking',
    response_model=GetTrackingOut,
    summary='Alliance tracking',
)
def get_alliance_tracking(
        alliance_id: int,
        tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Reports which member (of a given alliance) have a valid refresh token
    attacked to them, and which do not. Requires a clearance level of 3 and
    having authority over this alliance.
    """
    alliance: Alliance = Alliance.objects(alliance_id=alliance_id).get()
    assert_has_clearance(tkn.owner, 'sni.track_alliance', alliance.ceo)
    return GetTrackingOut.from_user_iterator(alliance.user_iterator())