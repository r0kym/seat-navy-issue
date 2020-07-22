"""
API Server
"""

import asyncio
import logging
from multiprocessing import Process

from fastapi import FastAPI

import uvicorn
import yaml

import sni.conf as conf
from sni.api.routers.coalition import router as router_coalition
from sni.api.routers.crash import router as router_crash
from sni.api.routers.esi import router as router_esi
from sni.api.routers.group import router as router_group
from sni.api.routers.sde import router as router_sde
from sni.api.routers.system import router as router_system
from sni.api.routers.token import router as router_token
from sni.api.routers.user import router as router_user

app = FastAPI()

app.include_router(
    router_coalition,
    prefix='/coalition',
    tags=['Coalition management'],
)

app.include_router(
    router_crash,
    prefix='/crash',
    tags=['Crash reports'],
)

if conf.get('discord.enabled'):
    from sni.api.routers.discord import router as router_discord
    app.include_router(
        router_discord,
        prefix='/discord',
        tags=['Discord'],
    )

app.include_router(router_esi)

app.include_router(
    router_group,
    prefix='/group',
    tags=['Group management'],
)

if conf.get('teamspeak.enabled'):
    from sni.api.routers.teamspeak import router as router_teamspeak
    app.include_router(
        router_teamspeak,
        prefix='/teamspeak',
        tags=['Teamspeak'],
    )

app.include_router(
    router_sde,
    prefix='/sde',
    tags=['SDE methods'],
)

app.include_router(
    router_system,
    prefix='/system',
    tags=['System administration'],
)

app.include_router(
    router_token,
    prefix='/token',
    tags=['Authentication & tokens'],
)

app.include_router(
    router_user,
    prefix='/user',
    tags=['User management'],
)


@app.get('/ping', tags=['Testing'], summary='Replies "pong"')
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


def _start_api_server():
    """
    Starts the API server for real. See
    :meth:`sni.api.server.start_api_server`.
    """
    log_level = str(conf.get('general.logging_level')).upper()
    log_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                '()': 'uvicorn.logging.DefaultFormatter',
                'fmt': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                'use_colors': None,
            },
            'access': {
                '()':
                'uvicorn.logging.AccessFormatter',
                'fmt': ('%(levelprefix)s %(client_addr)s - "%(request_line)s" '
                        '%(status_code)s'),
            },
        },
        'handlers': {
            'default': {
                'formatter': 'default',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stderr',
            },
            'access': {
                'formatter': 'access',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': log_level,
            },
            'uvicorn.error': {
                'level': log_level,
            },
            'uvicorn.access': {
                'handlers': ['access'],
                'level': log_level,
                'propagate': False,
            },
        },
    }
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    logging.info(
        'Starting API server on %s:%s',
        conf.get('general.host'),
        conf.get('general.port'),
    )
    try:
        uvicorn.run(
            'sni.api.server:app',
            host=conf.get('general.host'),
            log_config=log_config,
            log_level=log_level.lower(),
            port=conf.get('general.port'),
        )
    finally:
        logging.info('API server stopped')


def start_api_server():
    """
    Runs the API server in a dedicated process.
    """
    Process(
        daemon=True,
        name='api_server',
        target=_start_api_server,
    ).start()
