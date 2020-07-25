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

from sni.api.models import CrashReport

from .common import BSONObjectId

router = APIRouter()


class GetCrashReportRequestOut(pdt.BaseModel):
    """
    Embedded model for reponses for ``GET /crash/{crash_report_id}``.
    """
    headers: Optional[dict]
    method: str
    params: Optional[Any]
    url: str


class GetCrashReportTokenUserOut(pdt.BaseModel):
    """
    Embedded model for reponses for ``GET /crash/{crash_report_id}``.
    """
    authorized_to_login: bool
    character_id: int
    character_name: str
    clearance_level: int
    created_on: datetime
    updated_on: datetime


class GetCrashReportTokenOut(pdt.BaseModel):
    """
    Embedded model for reponses for ``GET /crash/{crash_report_id}``.
    """
    created_on: datetime
    expires_on: Optional[datetime]
    owner: GetCrashReportTokenUserOut
    token_type: str
    uuid: str


class GetCrashReportOut(pdt.BaseModel):
    """
    Response model for response for ``GET /crash/{crash_report_id}``.
    """
    id: str
    request: GetCrashReportRequestOut
    timestamp: datetime
    token: GetCrashReportTokenOut
    trace: List[str]

    @staticmethod
    def from_record(crash: CrashReport) -> 'GetCrashReportOut':
        """
        Converts a document of the crash report collection to a response model.
        """
        return GetCrashReportOut(
            id=str(crash.pk),
            request=GetCrashReportRequestOut(
                headers=crash.request.headers,
                method=crash.request.method,
                params=crash.request.params,
                url=crash.request.url,
            ),
            timestamp=crash.timestamp,
            trace=crash.trace,
            token=GetCrashReportTokenOut(
                created_on=crash.token.created_on,
                expires_on=crash.token.expires_on,
                owner=GetCrashReportTokenUserOut(
                    authorized_to_login=crash.token.owner.authorized_to_login,
                    character_id=crash.token.owner.character_id,
                    character_name=crash.token.owner.character_name,
                    clearance_level=crash.token.owner.clearance_level,
                    created_on=crash.token.owner.created_on,
                    updated_on=crash.token.owner.updated_on,
                ),
                token_type=crash.token.token_type,
                uuid=str(crash.token.uuid),
            ),
        )


class GetCrashReportShortOut(pdt.BaseModel):
    """
    Model for an element of a ``GET /crash`` response
    """
    character_id: int
    id: str
    timestamp: datetime
    url: str


def crash_report_record_to_short_response(
        crash: CrashReport) -> GetCrashReportShortOut:
    """
    Converts a document of the crash report collection to a short response
    model.
    """
    return GetCrashReportShortOut(
        character_id=crash.token.owner.character_id,
        id=str(crash.pk),
        timestamp=crash.timestamp,
        url=crash.request.url,
    )


@router.delete(
    '/{crash_report_id}',
    summary='Delete a crash report',
)
def delete_crash_report(
        crash_report_id: BSONObjectId,
        tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Deletes a crash report. Requires a clearance level of 10.
    """
    assert_has_clearance(tkn.owner, 'sni.delete_crash_report')
    CrashReport.objects.get(pk=crash_report_id).delete()


@router.get(
    '',
    response_model=List[GetCrashReportShortOut],
    summary='Get the list of the 50 most recent crash reports',
)
def get_crash_reports(tkn: Token = Depends(from_authotization_header_nondyn)):
    """
    Get the list of the 50 most recent crash reports, sorted from most to least
    recent. Requires a clearance level of 10.
    """
    assert_has_clearance(tkn.owner, 'sni.read_crash_report')
    return [
        crash_report_record_to_short_response(crash)
        for crash in CrashReport.objects().order_by('-timestamp')[:50]
    ]


@router.get(
    '/{crash_report_id}',
    response_model=GetCrashReportOut,
    summary='Get a crash report',
)
def get_crash_report(
        crash_report_id: BSONObjectId,
        tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Gets a crash report from its id. Requires a clearance level of 10.
    """
    assert_has_clearance(tkn.owner, 'sni.read_crash_report')
    return GetCrashReportOut.from_record(
        CrashReport.objects.get(pk=crash_report_id))
