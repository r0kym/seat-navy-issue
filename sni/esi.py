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
import jwt

import sni.conf as conf


def esi_request(method: str,
                endpoint: str,
                token: Optional[str] = None) -> Dict[str, Any]:
    """
    Makes a request to EVE ESI.
    """
    function = {
        'get': requests.get,
        'post': requests.post,
    }.get(method)
    function = cast(Optional[Callable[..., Dict[str, Any]]], function)
    if not function:
        raise ValueError(f'Unsupported HTTP method {method}')
    headers = {
        'Accept-Encoding': 'gzip',
        'accept': 'application/json',
        'User-Agent': 'seat-navy-issue',
    }
    if token:
        headers['Authorization'] = 'Bearer ' + token
    params = {'datasource': 'tranquility'}
    response = function(
        'https://esi.evetech.net/v5' + endpoint,
        headers=headers,
        params=params,
    )
    return response.json()


def get(endpoint: str, token: Optional[str] = None) -> Dict[str, Any]:
    """
    Issues a ``GET`` request to EVE ESI.
    """
    return esi_request('get', endpoint, token)


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


def get_basic_authorization_code() -> str:
    """
    Returns an authorization code derived from the ESI ``client_id`` and
    ``client_secret``.

    More precisely, it is::

        urlsafe_b64encode('<client_id>:<client_secret>')

    """
    authorization = str(conf.get('esi.client_id')) + ':' + str(
        conf.get('esi.client_secret'))
    return urlsafe_b64encode(authorization.encode()).decode()


def post(endpoint: str, token: Optional[str] = None) -> Dict[str, Any]:
    """
    Issues a ``POST`` request to EVE ESI.
    """
    return esi_request('post', endpoint, token)


def process_sso_authorization_code(code: str, state: str) -> bool:
    """
    Gets an access token (along with its refresh token) from an EVE SSO
    authorization code.

    A token document issued by the ESI looks like this::

        {
            "access_token": "jZOzkRtA8B...LQJg2",
            "token_type": "Bearer",
            "expires_in": 1199,
            "refresh_token": "RGuc...w1"
        }

    Returns:
        bool: Wether the authentication was successful.

    Reference:
        `esi-docs <https://docs.esi.evetech.net/docs/sso/web_based_sso_flow.html>`

    Todo:
        Validate the ESI JWT token
    """
    data = {
        'code': code,
        'grant_type': 'authorization_code',
    }
    headers = {
        'Authorization': 'Basic ' + get_basic_authorization_code(),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'login.eveonline.com',
    }
    response = requests.post(
        'https://login.eveonline.com/v2/oauth/token',
        headers=headers,
        data=data,
    )
    response_json = response.json()
    if 'access_token' not in response_json:
        return False
    decoded = jwt.decode(response_json['access_token'], verify=False)
    # pylint: disable=bad-str-strip-call
    character_id = str(decoded['sub']).strip('CHARACTER:EVE:')
    logging.info(
        'Successfully obtained access token for character %s (%s)',
        decoded['name'],
        character_id,
    )
    return True


def refresh_access_token(refresh_token: str) -> bool:
    """
    Refreshes an access token.

    Returns:
        Wether the refresh was successful.

    Reference:
        `esi-docs <https://docs.esi.evetech.net/docs/sso/refreshing_access_tokens.html>`_
    """
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'login.eveonline.com',
        'Authorization': 'Basic ' + get_basic_authorization_code()
    }
    response = requests.post(
        'https://login.eveonline.com/v2/oauth/token',
        headers=headers,
        data=data,
    )
    response_json = response.json()
    if 'access_token' not in response_json:
        return False
    decoded = jwt.decode(response_json['access_token'], verify=False)
    # pylint: disable=bad-str-strip-call
    character_id = str(decoded['sub']).strip('CHARACTER:EVE:')
    logging.info(
        'Successfully refreshed access token for character %s (%s)',
        decoded['name'],
        character_id,
    )
    return True
