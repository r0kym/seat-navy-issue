"""
EVE ESI module
"""

from typing import (Any, Callable, cast, Dict, Optional)
from urllib.parse import urljoin

import rest

ESI_BASE_URL = 'https://esi.evetech.net/latest/'


def delete(token: Optional[str] = None) -> Dict[str, Any]:
    """
    Issues a ``DELETE`` request to EVE ESI.
    """
    return do_request('put', token)


def do_request(method: str, token: Optional[str] = None) -> Dict[str, Any]:
    """
    Actually makes request.
    """
    function = {
        'delete': rest.delete,
        'get': rest.get,
        'post': rest.post,
        'put': rest.put
    }.get(method.lower())
    function = cast(Optional[Callable[..., Dict[str, Any]]], function)
    if not function:
        raise ValueError(f'Unknown HTTP method {method}')
    url = urljoin(ESI_BASE_URL, method)
    headers = {
        'Accept-Encoding': 'gzip',
        'accept': 'application/json',
        'User-Agent': 'seat-navy-issue'
    }
    params = {'datasource': 'tranquility'}
    if token:
        params['token'] = token
    return function(url, headers=headers, params=params)


def get(token: Optional[str] = None) -> Dict[str, Any]:
    """
    Issues a ``GET`` request to EVE ESI.
    """
    return do_request('get', token)


def post(token: Optional[str] = None) -> Dict[str, Any]:
    """
    Issues a ``POST`` request to EVE ESI.
    """
    return do_request('post', token)


def put(token: Optional[str] = None) -> Dict[str, Any]:
    """
    Issues a ``PUT`` request to EVE ESI.
    """
    return do_request('put', token)
