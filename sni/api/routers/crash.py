"""
Crash reports paths
"""

from datetime import datetime
from typing import Any, List, Optional

from fastapi import APIRouter, Depends
import pydantic as pdt

from sni.uac.clearance import assert_has_clearance
from sni.uac.token import (
    from_authotization_header_nondyn,
    Token,
)

from sni.api.models import (
    CrashReport,
    CrashReportRequest,
    CrashReportToken,
)

from .common import BSONObjectId
from .user import GetUserOut, GetUserShortOut

router = APIRouter()


class GetCrashReportRequestOut(pdt.BaseModel):
    """
    Embedded model for reponses for ``GET /crash/{crash_report_id}``.
    """

    headers: Optional[dict]
    method: str
    params: Optional[Any]
    url: str

    @staticmethod
    def from_record(request: CrashReportRequest) -> "GetCrashReportRequestOut":
        """
        Converts a :class:`sni.api.models.CrashReportRequest` to a
        :class:`sni.api.routers.GetCrashReportRequestOut`.
        """
        return GetCrashReportRequestOut(
            headers=request.headers,
            method=request.method,
            params=request.params,
            url=request.url,
        )


class GetCrashReportTokenOut(pdt.BaseModel):
    """
    Embedded model for reponses for ``GET /crash/{crash_report_id}``.
    """

    created_on: datetime
    expires_on: Optional[datetime]
    owner: GetUserOut
    token_type: str
    uuid: str

    @staticmethod
    def from_record(token: CrashReportToken) -> "GetCrashReportTokenOut":
        """
        Reports basic informations about a token used at the moment of a crash.
        """
        return GetCrashReportTokenOut(
            created_on=token.created_on,
            expires_on=token.expires_on,
            owner=GetUserOut.from_record(token.owner),
            token_type=token.token_type,
            uuid=str(token.uuid),
        )


class GetCrashReportOut(pdt.BaseModel):
    """
    Response model for response for ``GET /crash/{crash_report_id}``.
    """

    id: str
    request: GetCrashReportRequestOut
    timestamp: datetime
    token: Optional[GetCrashReportTokenOut]
    trace: List[str]

    @staticmethod
    def from_record(crash: CrashReport) -> "GetCrashReportOut":
        """
        Converts a document of the crash report collection to a response model.
        """
        return GetCrashReportOut(
            id=str(crash.pk),
            request=GetCrashReportRequestOut.from_record(crash.request),
            timestamp=crash.timestamp,
            trace=crash.trace,
            token=GetCrashReportTokenOut.from_record(crash.token)
            if crash.token is not None
            else None,
        )


class GetCrashReportShortOut(pdt.BaseModel):
    """
    Model for an element of a ``GET /crash`` response
    """

    user: Optional[GetUserShortOut]
    id: str
    timestamp: datetime
    url: str

    @staticmethod
    def from_record(crash: CrashReport) -> "GetCrashReportShortOut":
        """
        Converts a document of the crash report collection to a short response
        model.
        """
        return GetCrashReportShortOut(
            user=GetUserShortOut.from_record(crash.token.owner)
            if crash.token is not None
            else None,
            id=str(crash.pk),
            timestamp=crash.timestamp,
            url=crash.request.url,
        )


@router.delete(
    "/{crash_report_id}", summary="Delete a crash report",
)
def delete_crash_report(
    crash_report_id: BSONObjectId,
    tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Deletes a crash report. Requires a clearance level of 10.
    """
    assert_has_clearance(tkn.owner, "sni.delete_crash_report")
    CrashReport.objects.get(pk=crash_report_id).delete()


@router.get(
    "",
    response_model=List[GetCrashReportShortOut],
    summary="Get the list of the 50 most recent crash reports",
)
def get_crash_reports(tkn: Token = Depends(from_authotization_header_nondyn)):
    """
    Get the list of the 50 most recent crash reports, sorted from most to least
    recent. Requires a clearance level of 10.
    """
    assert_has_clearance(tkn.owner, "sni.read_crash_report")
    return [
        GetCrashReportShortOut.from_record(crash)
        for crash in CrashReport.objects().order_by("-timestamp")[:50]
    ]


@router.get(
    "/{crash_report_id}",
    response_model=GetCrashReportOut,
    summary="Get a crash report",
)
def get_crash_report(
    crash_report_id: BSONObjectId,
    tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Gets a crash report from its id. Requires a clearance level of 10.
    """
    assert_has_clearance(tkn.owner, "sni.read_crash_report")
    return GetCrashReportOut.from_record(
        CrashReport.objects.get(pk=crash_report_id)
    )
