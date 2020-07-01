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
import requests.exceptions
import uvicorn
import yaml

import sni.conf as conf
import sni.routers.coalition
import sni.routers.esi
import sni.routers.group
import sni.routers.token
import sni.routers.user

app = FastAPI()
app.include_router(
    sni.routers.coalition.router,
    prefix='/coalition',
    tags=['Coalition management'],
)
app.include_router(sni.routers.esi.router)
app.include_router(
    sni.routers.group.router,
    prefix='/group',
    tags=['Group management'],
)
if conf.get('teamspeak.enabled'):
    import sni.routers.teamspeak
    app.include_router(
        sni.routers.teamspeak.router,
        prefix='/teamspeak',
        tags=['Teamspeak'],
    )
app.include_router(
    sni.routers.token.router,
    prefix='/token',
    tags=['Authentication & tokens'],
)
app.include_router(
    sni.routers.user.router,
    prefix='/user',
    tags=['User management'],
)


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


@app.exception_handler(PermissionError)
def permission_error_handler(_request: requests.Request,
                             error: PermissionError):
    """
    Catches :class:`PermissionError` exceptions and forwards them as
    ``403``'s.
    """
    if conf.get('general.debug'):
        content = {'details': 'Insufficient clearance level: ' + str(error)}
    else:
        content = {'details': 'Insufficient clearance level'}
    return JSONResponse(
        content=content,
        status_code=status.HTTP_403_FORBIDDEN,
    )


@app.exception_handler(requests.exceptions.HTTPError)
def requests_httperror_handler(_request: requests.Request,
                               error: requests.exceptions.HTTPError):
    """
    Catches :class:`requests.exceptions.HTTPError` exceptions and forwards them
    as ``500``'s.
    """
    if conf.get('general.debug') and error.request is not None:
        req: requests.Request = error.request
        content = {
            'details':
            f'Failed to issue {req.method} to "{req.url}": {str(error)}'
        }
    return JSONResponse(
        content=content,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
    summary='Replies "pong"'
)
async def get_ping():
    """
    Replies ``pong``. That is all.
    """
    return 'pong'


def print_openapi_spec() -> None:
    """
    Print the OpenAPI specification of the server in YAML.
    """
    print(yaml.dump(app.openapi()))


def start():
    """
    Runs the API server.
    """
    logging.info('Starting API server on %s:%s', conf.get('general.host'),
                 conf.get('general.port'))
    try:
        uvicorn.run(
            'sni.apiserver:app',
            host=conf.get('general.host'),
            log_level='debug' if conf.get('general.debug') else 'info',
            port=conf.get('general.port'),
        )
    finally:
        logging.info('API server stopped')
