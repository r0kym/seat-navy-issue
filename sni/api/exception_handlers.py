"""
FastAPI exception handlers
"""

from traceback import format_exception
from typing import Optional
import logging

from fastapi import status
from fastapi.responses import JSONResponse
from requests import Request
from requests.exceptions import HTTPError
import mongoengine as me
import sentry_sdk

from sni.uac.token import from_authotization_header
from sni.conf import CONFIGURATION as conf

from .models import CrashReport, CrashReportRequest, CrashReportToken
from .server import app


def crash_report(request: Request, error: Exception) -> CrashReport:
    """
    Constructs a crash report
    """
    try:
        token = from_authotization_header(request.headers["authorization"])
        crtoken: Optional[CrashReportToken] = CrashReportToken(
            created_on=token.created_on,
            expires_on=token.expires_on,
            owner=token.owner,
            token_type=token.token_type,
            uuid=token.uuid,
        )
    except Exception:
        crtoken = None
    trace = format_exception(
        etype=type(error), value=error, tb=error.__traceback__,
    )
    return CrashReport(
        request=CrashReportRequest(
            headers=request.headers if hasattr(request, "headers") else None,
            method=str(request.method) if hasattr(request, "method") else "?",
            params=request.params if hasattr(request, "params") else None,
            url=str(request.url) if hasattr(request, "url") else "?",
        ),
        token=crtoken,
        trace=trace,
    )


def send_exception_to_sentry(error: Exception, *args, **kwargs):
    """
    If the configuration field `general.sentry_dsn`, dispatches the exception
    to Sentry
    """
    if conf.general.sentry_dsn is not None:
        sentry_sdk.capture_exception(error, *args, **kwargs)


@app.exception_handler(LookupError)
@app.exception_handler(me.DoesNotExist)
def does_not_exist_exception_handler(_request: Request, error: Exception):
    """
    Catches :class:`me.DoesNotExist` exceptions and forwards them as
    ``404``'s.
    """
    send_exception_to_sentry(error)
    return JSONResponse(
        content={"details": str(error)} if conf.general.debug else None,
        status_code=status.HTTP_404_NOT_FOUND,
    )


@app.exception_handler(PermissionError)
def permission_error_handler(_request: Request, error: PermissionError):
    """
    Catches :class:`PermissionError` exceptions and forwards them as
    ``403``'s.
    """
    send_exception_to_sentry(error)
    content = {"details": "Insufficient clearance level"}
    if conf.general.debug:
        content["details"] += ": " + str(error)
    return JSONResponse(
        content=content, status_code=status.HTTP_403_FORBIDDEN,
    )


@app.exception_handler(HTTPError)
def requests_httperror_handler(_request: Request, error: HTTPError):
    """
    Catches :class:`requests.exceptions.HTTPError` exceptions and forwards them
    as ``500``'s.
    """
    send_exception_to_sentry(error)
    content = None
    if conf.general.debug and error.request is not None:
        req: Request = error.request
        content = {
            "details": f'Failed to issue {req.method} to "{req.url}"'
            + f": {str(error)}"
        }
    return JSONResponse(
        content=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@app.exception_handler(Exception)
def exception_handler(request: Request, error: Exception):
    """
    Global exception handler. Exception reaching this handler are considered to
    be crashes. A crash report is generated, and returned if SNI runs in debug
    mode.
    """
    send_exception_to_sentry(error)
    crash = crash_report(request, error)
    crash.save()
    logging.error(
        "The following crash report has been saved with id %s", str(crash.pk)
    )
    content = (
        crash.to_dict()
        if conf.general.debug
        else {"crash_report_id": str(crash.pk)}
    )
    return JSONResponse(
        content=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
