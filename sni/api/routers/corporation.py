"""
Corporation management paths
"""

from datetime import datetime
from typing import Dict, Iterator, List, Optional

from fastapi import APIRouter, Depends
import pydantic as pdt

from sni.esi.models import EsiScope
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


class GetCorporationOut(pdt.BaseModel):
    """
    Corporation data
    """

    alliance_id: Optional[int]
    alliance_name: Optional[str]
    authorized_to_login: Optional[bool]
    ceo_character_id: int
    ceo_character_name: str
    corporation_id: int
    corporation_name: str
    cumulated_mandatory_esi_scopes: List[EsiScope]
    mandatory_esi_scopes: List[EsiScope]
    ticker: str
    updated_on: datetime

    @staticmethod
    def from_record(corporation: Corporation) -> "GetCorporationOut":
        """
        Converts an instance of :class:`sni.user.models.Corporation` to
        :class:`sni.api.routers.corporation.GetCorporationOut`
        """
        return GetCorporationOut(
            alliance_id=corporation.alliance.alliance_id
            if corporation.alliance is not None
            else None,
            alliance_name=corporation.alliance.alliance_name
            if corporation.alliance is not None
            else None,
            authorized_to_login=corporation.authorized_to_login,
            ceo_character_id=corporation.ceo.character_id,
            ceo_character_name=corporation.ceo.character_name,
            corporation_id=corporation.corporation_id,
            corporation_name=corporation.corporation_name,
            cumulated_mandatory_esi_scopes=list(
                corporation.cumulated_mandatory_esi_scopes()
            ),
            mandatory_esi_scopes=corporation.mandatory_esi_scopes,
            ticker=corporation.ticker,
            updated_on=corporation.updated_on,
        )


class GetCorporationShortOut(pdt.BaseModel):
    """
    Short corporation description
    """

    corporation_id: int
    corporation_name: str

    @staticmethod
    def from_record(corporation: Corporation) -> "GetCorporationShortOut":
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
    def from_user_iterator(iterator: Iterator[User]) -> "GetTrackingOut":
        """
        Creates a tracking response from a user iterator. See
        :meth:`sni.esi.token.tracking_status`
        """
        result = GetTrackingOut()
        ldict: Dict[int, List[GetUserShortOut]] = {
            TrackingStatus.HAS_NO_REFRESH_TOKEN: result.no_refresh_token,
            TrackingStatus.ONLY_HAS_INVALID_REFRESH_TOKEN: result.invalid_refresh_token,
            TrackingStatus.HAS_A_VALID_REFRESH_TOKEN: result.valid_refresh_token,
        }
        for usr in iterator:
            status = tracking_status(usr)
            ldict[status].append(GetUserShortOut.from_record(usr))
        return result


class PutCorporationIn(pdt.BaseModel):
    """
    Model for ``PUT /corporation/{corporation_id}`` requests
    """

    authorized_to_login: Optional[bool]
    mandatory_esi_scopes: Optional[List[EsiScope]]


@router.get(
    "",
    response_model=List[GetCorporationShortOut],
    summary="Get the list of corporations",
)
def get_corporations(tkn: Token = Depends(from_authotization_header_nondyn),):
    """
    Gets the list of corporations registered in this instance. Requires a
    clearance level of 0 or more.
    """
    assert_has_clearance(tkn.owner, "sni.read_corporation")
    return [
        GetCorporationShortOut.from_record(corporation)
        for corporation in Corporation.objects().order_by("corporation_name")
    ]


@router.get(
    "/{corporation_id}",
    response_model=GetCorporationOut,
    summary="Get informations about a corporation",
)
def get_corporation(
    corporation_id: int,
    tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Get informations about a corporation. Note that this corporation must be
    registered on SNI
    """
    assert_has_clearance(tkn.owner, "sni.read_corporation")
    corporation = Corporation.objects(corporation_id=corporation_id).get()
    return GetCorporationOut.from_record(corporation)


@router.post(
    "/{corporation_id}",
    response_model=GetCorporationOut,
    summary="Manually fetch a corporation from the ESI",
)
def post_corporation(
    corporation_id: int,
    tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Manually fetches a corporation from the ESI. Requires a clearance level of
    8 or more.
    """
    assert_has_clearance(tkn.owner, "sni.fetch_corporation")
    corporation = ensure_corporation(corporation_id)
    return GetCorporationOut.from_record(corporation)


@router.put(
    "/{corporation_id}",
    response_model=GetCorporationOut,
    summary="Modify a corporation registered on SNI",
)
def put_corporation(
    corporation_id: int,
    data: PutCorporationIn,
    tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Modify a corporation registered on SNI. Note that it does not modify it on
    an ESI level. Requires a clearance level of 4 or more.
    """
    corporation: Corporation = Corporation.objects(
        corporation_id=corporation_id
    ).get()
    assert_has_clearance(tkn.owner, "sni.update_corporation", corporation.ceo)
    corporation.authorized_to_login = data.authorized_to_login
    if data.mandatory_esi_scopes is not None:
        corporation.mandatory_esi_scopes = data.mandatory_esi_scopes
    corporation.save()
    return GetCorporationOut.from_record(corporation)


@router.get(
    "/{corporation_id}/tracking",
    response_model=GetTrackingOut,
    summary="Corporation tracking",
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
        corporation_id=corporation_id
    ).get()
    assert_has_clearance(tkn.owner, "sni.track_corporation", corporation.ceo)
    return GetTrackingOut.from_user_iterator(corporation.user_iterator())
