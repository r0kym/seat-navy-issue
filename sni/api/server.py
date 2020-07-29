"""
API Server
"""

import logging
from typing import List

from fastapi import FastAPI
import pydantic as pdt
import uvicorn
import yaml

from sni.conf import CONFIGURATION as conf
from sni.utils import object_from_name

app = FastAPI()


class RouterConfig(pdt.BaseModel):
    """
    Basic router configuration
    """
    include: bool = True
    kwargs: dict
    prefix: str
    router: str

    def add_to_application(self, application: FastAPI) -> None:
        """
        Adds the current router to the FastAPI application.
        """
        logging.debug('Adding router %s at prefix %s', self.router,
                      self.prefix)
        application.include_router(
            object_from_name(self.router),
            prefix=self.prefix,
            **self.kwargs,
        )


ROUTERS: List[RouterConfig] = [
    RouterConfig(
        router='sni.api.routers.alliance:router',
        prefix='/alliance',
        kwargs={'tags': ['Alliance management']},
    ),
    RouterConfig(
        router='sni.api.routers.callback:router',
        prefix='/callback',
        kwargs={'tags': ['Callbacks']},
    ),
    RouterConfig(
        router='sni.api.routers.coalition:router',
        prefix='/coalition',
        kwargs={'tags': ['Coalition management']},
    ),
    RouterConfig(
        router='sni.api.routers.corporation:router',
        prefix='/corporation',
        kwargs={'tags': ['Corporation management']},
    ),
    RouterConfig(
        router='sni.api.routers.crash:router',
        prefix='/crash',
        kwargs={'tags': ['Crash reports']},
    ),
    RouterConfig(
        router='sni.api.routers.discord:router',
        prefix='/discord',
        kwargs={'tags': ['Discord']},
        include=conf.discord.enabled,
    ),
    RouterConfig(
        router='sni.api.routers.esi:router',
        prefix='/esi',
        kwargs={'tags': ['ESI']},
    ),
    RouterConfig(
        router='sni.api.routers.group:router',
        prefix='/group',
        kwargs={'tags': ['Group management']},
    ),
    RouterConfig(
        router='sni.api.routers.teamspeak:router',
        prefix='/teamspeak',
        kwargs={'tags': ['Teamspeak']},
        include=conf.teamspeak.enabled,
    ),
    RouterConfig(
        router='sni.api.routers.system:router',
        prefix='/system',
        kwargs={'tags': ['System administration']},
    ),
    RouterConfig(
        router='sni.api.routers.token:router',
        prefix='/token',
        kwargs={'tags': ['Authentication & tokens']},
    ),
    RouterConfig(
        router='sni.api.routers.user:router',
        prefix='/user',
        kwargs={'tags': ['User management']},
    ),
]


def add_included_routers():
    """
    Adds all routers whose ``include`` field is ``True``
    """
    for router in ROUTERS:
        if router.include:
            router.add_to_application(app)


# @app.get('/ping', tags=['Testing'], summary='Replies "pong"')
# async def get_ping():
#     """
#     Replies ``pong``. That is all.
#     """
#     return 'pong'


def print_openapi_spec() -> None:
    """
    Print the OpenAPI specification of the server in YAML.
    """
    for router in ROUTERS:
        if not router.include:
            router.add_to_application(app)
    print(yaml.dump(app.openapi()))


def start_api_server():
    """
    Starts the API server for real. See
    :meth:`sni.api.server.start_api_server`.
    """
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
                'level': conf.general.logging_level.upper(),
            },
            'uvicorn.error': {
                'level': conf.general.logging_level.upper(),
            },
            'uvicorn.access': {
                'handlers': ['access'],
                'level': conf.general.logging_level.upper(),
                'propagate': False,
            },
        },
    }
    logging.info(
        'Starting API server on %s:%s',
        conf.general.host,
        conf.general.port,
    )
    try:
        uvicorn.run(
            'sni.api.server:app',
            host=str(conf.general.host),
            log_config=log_config,
            log_level=conf.general.logging_level,
            port=conf.general.port,
        )
    finally:
        logging.info('API server stopped')


add_included_routers()
