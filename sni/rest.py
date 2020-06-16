"""
REST API module

Declares various functions for **issuing** API calls returning JSON documents.
"""

from typing import (Any, Callable, cast, Dict, Optional)

import requests


def delete(url: str, *args, **kwargs) -> Dict[str, Any]:
    """
    Wrapper for :func:`requests.delete`.
    """
    return do_request('delete', url, *args, **kwargs)


def do_request(method: str, url: str, *args, **kwargs) -> Dict[str, Any]:
    """
    Actually makes request.
    """
    function = {
        'delete': requests.delete,
        'get': requests.get,
        'post': requests.post,
        'put': requests.put
    }.get(method.lower())
    function = cast(Optional[Callable[..., requests.Response]], function)
    if not function:
        raise ValueError(f'Unknown HTTP method {method}')
    response = function(url, *args, **kwargs)
    return response.json()


def get(url: str, *args, **kwargs) -> Dict[str, Any]:
    """
    Wrapper for :func:`requests.get`.
    """
    return do_request('get', url, *args, **kwargs)


def post(url: str, *args, **kwargs) -> Dict[str, Any]:
    """
    Wrapper for :func:`requests.post`.
    """
    return do_request('post', url, *args, **kwargs)


def put(url: str, *args, **kwargs) -> Dict[str, Any]:
    """
    Wrapper for :func:`requests.put`.
    """
    return do_request('put', url, *args, **kwargs)
