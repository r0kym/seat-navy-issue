# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
"""
API Server
"""

import logging
import traceback

from fastapi import (
    FastAPI,
    status,
)
from fastapi.responses import JSONResponse
import mongoengine
import requests
import yaml

import sni.conf as conf

import sni.routers.esi
import sni.routers.token

app = FastAPI()
app.include_router(sni.routers.esi.router)
app.include_router(sni.routers.token.router)


@app.exception_handler(mongoengine.DoesNotExist)
def does_not_exist_exception_handler(_request: requests.Request,
                                     error: Exception):
    """
    Catches :class:`mongoengine.DoesNotExist` exceptions and forwards them as
    ``404``'s.
    """
    content = None
    if conf.get('general.debug'):
        content = {'details': str(error)}
    return JSONResponse(
        content=content,
        status_code=status.HTTP_404_NOT_FOUND,
    )


@app.exception_handler(Exception)
def exception_handler(_request: requests.Request, error: Exception):
    """
    Global exception handler.

    Prints trace for all others.
    """
    content = None
    if conf.get('general.debug'):
        traceback_data = traceback.format_exception(
            etype=type(error),
            value=error,
            tb=error.__traceback__,
        )
        logging.error(''.join(traceback_data))
        content = traceback_data
    return JSONResponse(
        content=content,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@app.get(
    '/ping',
    tags=['Testing'],
)
async def get_ping():
    """
    Returns ``pong``.
    """
    return 'pong'


def print_openapi_spec() -> None:
    """
    Print the OpenAPI specification of the server in YAML.
    """
    print(yaml.dump(app.openapi()))
