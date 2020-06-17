"""
EVE ESI module
"""

from base64 import urlsafe_b64encode
import logging
from typing import (
    Any,
    Callable,
    cast,
    Dict,
    Optional,
    List,
)
from urllib.parse import urljoin

import requests

import sni.conf as conf
import sni.rest as rest

ESI_BASE_URL = 'https://esi.evetech.net/latest/'


def get_auth_url(esi_scopes: List[str] = ['publicData'],
                 state: str = 'None') -> str:
    """
    Returns an EVE SSO login url based on the scopes passed in argument.

    Args:
        esi_scopes: List of esi scope
        state: A state string (default: ``None``)

    Returns:
        A url in string form
    """
    if not esi_scopes:
        logging.warning(
            'Scope list cannot be empty, replaced by [\'publicData\']')
        esi_scopes = ['publicData']
    params = {
        'client_id': conf.get('esi.client_id'),
        'redirect_uri': urljoin(conf.get('general.root_url'), '/callback/esi'),
        'response_type': 'code',
        'scope': ' '.join(esi_scopes),
        'state': state,
    }
    request = requests.Request(
        'GET',
        'https://login.eveonline.com/v2/oauth/authorize/',
        params=params,
    )
    url = request.prepare().url
    if not url:
        raise RuntimeError('Could not construct a valid auth URL')
    return url


def process_sso_authorization_code(code: str, state: str):
    """
    Gets an access token (along with its refresh token) from an EVE SSO
    authorization code.

    Reference:
        `OAuth 2.0 for Web Based Applications <https://docs.esi.evetech.net/docs/sso/web_based_sso_flow.html>`
    """
    data = {
        'code': code,
        'grant_type': 'authorization_code',
    }
    authorization = str(conf.get('esi.client_id')) + ':' + str(
        conf.get('esi.client_secret'))
    authorization_b64 = urlsafe_b64encode(authorization.encode()).decode()
    headers = {
        'Authorization': 'Basic ' + authorization_b64,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'login.eveonline.com',
    }
    logging.debug(headers)
    response_json = rest.post_json(
        'https://login.eveonline.com/v2/oauth/token',
        headers=headers,
        data=data,
    )
    from pprint import pprint
    pprint(response_json)


def do_request(method: str, token: Optional[str] = None) -> Dict[str, Any]:
    """
    Makes a request to EVE ESI.
    """
    function = {
        'get': rest.get_json,
        'post': rest.post_json,
    }.get(method)
    function = cast(Optional[Callable[..., Dict[str, Any]]], function)
    if not function:
        raise ValueError(f'Unsupported HTTP method {method}')
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
