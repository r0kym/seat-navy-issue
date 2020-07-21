"""
API Server
"""

import logging

from fastapi import FastAPI

import uvicorn
import yaml

import sni.conf as conf
import sni.api.routers.coalition
import sni.api.routers.crash
import sni.api.routers.esi
import sni.api.routers.group
import sni.api.routers.sde
import sni.api.routers.token
import sni.api.routers.user

app = FastAPI()

app.include_router(
    sni.api.routers.coalition.router,
    prefix='/coalition',
    tags=['Coalition management'],
)

app.include_router(
    sni.api.routers.crash.router,
    prefix='/crash',
    tags=['Crash reports'],
)

if conf.get('discord.enabled'):
    import sni.api.routers.discord
    app.include_router(
        sni.api.routers.discord.router,
        prefix='/discord',
        tags=['Discord'],
    )

app.include_router(sni.api.routers.esi.router)

app.include_router(
    sni.api.routers.group.router,
    prefix='/group',
    tags=['Group management'],
)

if conf.get('teamspeak.enabled'):
    import sni.api.routers.teamspeak
    app.include_router(
        sni.api.routers.teamspeak.router,
        prefix='/teamspeak',
        tags=['Teamspeak'],
    )

app.include_router(
    sni.api.routers.sde.router,
    prefix='/sde',
    tags=['SDE methods'],
)

app.include_router(
    sni.api.routers.token.router,
    prefix='/token',
    tags=['Authentication & tokens'],
)

app.include_router(
    sni.api.routers.user.router,
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


def start_api_server():
    """
    Runs the API server.
    """
    logging.info('Starting API server on %s:%s', conf.get('general.host'),
                 conf.get('general.port'))
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
