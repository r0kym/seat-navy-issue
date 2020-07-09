"""
EVE ESI (public API) layer
"""

import logging
import re
from typing import Optional

import mongoengine as me
from requests import request, Response

import sni.conf as conf

from .models import EsiPath

ESI_BASE = 'https://esi.evetech.net/'
ESI_SWAGGER = ESI_BASE + 'latest/swagger.json'


def esi_delete(path: str, token: Optional[str] = None, **kwargs) -> Response:
    """
    Wrapper for :meth:`sni.esi.esi.esi_request` for DELETE requests.
    """
    return esi_request('delete', path, token, **kwargs)


def esi_get(path: str, token: Optional[str] = None, **kwargs) -> Response:
    """
    Wrapper for :meth:`sni.esi.esi.esi_request` for GET requests.
    """
    return esi_request('get', path, token, **kwargs)


def esi_post(path: str, token: Optional[str] = None, **kwargs) -> Response:
    """
    Wrapper for :meth:`sni.esi.esi.esi_request` for POST requests.
    """
    return esi_request('post', path, token, **kwargs)


def esi_put(path: str, token: Optional[str] = None, **kwargs) -> Response:
    """
    Wrapper for :meth:`sni.esi.esi.esi_request` for PUT requests.
    """
    return esi_request('put', path, token, **kwargs)


def esi_request(http_method: str,
                path: str,
                token: Optional[str] = None,
                **kwargs) -> Response:
    """
    Makes an HTTP request to the ESI, and returns the response object.
    """
    kwargs['headers'] = {
        'Accept-Encoding': 'gzip',
        'accept': 'application/json',
        'User-Agent': 'SeAT Navy Issue @ ' + conf.get('general.root_url'),
        **kwargs.get('headers', {})
    }
    if token:
        kwargs['headers']['Authorization'] = 'Bearer ' + token
    response = request(http_method, ESI_BASE + path, **kwargs)
    response.raise_for_status()
    return response


def get_esi_path_scope(path: str) -> Optional[str]:
    """
    Returns the ESI scope that is required for a given ESI path.

    Raises :class:`mongoengine.DoesNotExist` if no suitable path is found.

    Examples:

        >>> get_esi_path_scope('latest/characters/0000000000/assets')
        'esi-assets.read_assets.v1'

        >>> get_esi_path_scope('latest/alliances')
        None
    """
    esi_path: EsiPath
    for esi_path in EsiPath.objects:
        # print(esi_path.to_json())
        if re.search(esi_path.path_re, path):
            return esi_path.scope
    raise me.DoesNotExist


def load_esi_openapi() -> None:
    """
    Loads the ESI Swagger API into the database.

    Should be called in the initialization stage.

    See also:
        :class:`sni.esi.esi.EsiPath`
        `EVE Swagger Interface <https://esi.evetech.net/ui>`_
        `EVE Swagger Interface (JSON) <https://esi.evetech.net/latest/swagger.json>`_
    """
    logging.info('Loading ESI swagger specifications %s', ESI_SWAGGER)
    swagger = request('GET', ESI_SWAGGER).json()
    base_path = swagger['basePath'][1:]
    for path, path_data in swagger['paths'].items():
        for method, method_data in path_data.items():
            full_path = base_path + path
            path_re = '^' + re.sub(r'{\w+_id}', '[^/]+', full_path) + '?$'
            scope = None
            for security in method_data.get('security', []):
                scope = security.get('evesso', [scope])[0]
            EsiPath.objects(
                http_method=method,
                path=full_path,
            ).update(
                set__http_method=method,
                set__path_re=path_re,
                set__path=full_path,
                set__scope=scope,
                set__version='latest',
                upsert=True,
            )
