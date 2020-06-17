"""
REST API module

Declares various functions for **issuing** API calls returning JSON documents.
"""

from typing import (Any, Callable, cast, Dict, Optional)

import requests


def request_json(method: str, url: str, *args, **kwargs) -> Dict[str, Any]:
    """
    Makes a request and expects a JSON response.
    """
    function = {
        'get': requests.get,
        'post': requests.post,
    }.get(method)
    function = cast(Optional[Callable[..., requests.Response]], function)
    if not function:
        raise ValueError(f'Unsupported HTTP method {method}')
    response = function(url, *args, **kwargs)
    return response.json()


def get_json(url: str, *args, **kwargs) -> Dict[str, Any]:
    """
    Wrapper for :func:`requests.get`.
    """
    return request_json('get', url, *args, **kwargs)


def post_json(url: str, *args, **kwargs) -> Dict[str, Any]:
    """
    Wrapper for :func:`requests.post`.
    """
    return request_json('post', url, *args, **kwargs)
