"""
Corporation management paths
"""

from typing import List

from fastapi import APIRouter, Depends
import pydantic as pdt

from sni.esi.token import EsiRefreshToken
from sni.uac.clearance import assert_has_clearance
from sni.uac.token import (
    from_authotization_header_nondyn,
    Token,
)
from sni.user.models import Corporation
from sni.user.user import ensure_corporation

router = APIRouter()


class GetCorporationTrackingOut(pdt.BaseModel):
    """
    Represents a corporation tracking response.
    """
    invalid_refresh_token: List[int] = []
    no_refresh_token: List[int] = []
    valid_refresh_token: List[int] = []


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
    response_model=GetCorporationTrackingOut,
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

    response = GetCorporationTrackingOut()
    for usr in corporation.user_iterator():

        query_set = EsiRefreshToken.objects(owner=usr)
        if query_set.count() == 0:
            response.no_refresh_token.append(usr.character_id)
            continue

        has_valid_refresh_token = False
        cumulated_mandatory_esi_scopes = usr.cumulated_mandatory_esi_scopes()
        for refresh_token in query_set:
            if cumulated_mandatory_esi_scopes <= set(refresh_token.scopes):
                has_valid_refresh_token = True
                break

        if has_valid_refresh_token:
            response.valid_refresh_token.append(usr.character_id)
        else:
            response.invalid_refresh_token.append(usr.character_id)

    return response
