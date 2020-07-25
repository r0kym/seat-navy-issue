"""
This module handles the communication with EVE SSO
"""

from base64 import urlsafe_b64encode
import logging
from typing import List
from urllib.parse import urljoin

from pydantic.error_wrappers import ValidationError
from requests.exceptions import HTTPError
import jwt
import pydantic as pdt
import requests

import sni.conf as conf


class AuthorizationCodeResponse(pdt.BaseModel):
    """
    A token document issued by the ESI looks like this::

        {
            "access_token": "jZOzkRtA8B...LQJg2",
            "token_type": "Bearer",
            "expires_in": 1199,
            "refresh_token": "RGuc...w1"
        }
    """
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str


class DecodedAccessToken(pdt.BaseModel):
    """
    Decoded access token issued by the ESI. Should look like this::

        {
            "scp": [
                "esi-skills.read_skills.v1",
                "esi-skills.read_skillqueue.v1"
            ],
            "jti": "998e12c7-3241-43c5-8355-2c48822e0a1b",
            "kid": "JWT-Signature-Key",
            "sub": "CHARACTER:EVE:123123",
            "azp": "my3rdpartyclientid",
            "name": "Some Bloke",
            "owner": "8PmzCeTKb4VFUDrHLc/AeZXDSWM=",
            "exp": 1534412504,
            "iss": "login.eveonline.com"
        }
    """
    azp: str
    exp: int
    iss: str
    jti: str
    kid: str
    name: str
    owner: str
    scp: List[str]
    sub: str

    @property
    def character_id(self) -> int:
        """
        Extracts the character ID from the ``sub`` field.
        """
        prefix = 'CHARACTER:EVE:'
        if not self.sub.startswith(prefix):
            raise ValueError('Unexpected "sub" field format: ' + self.sub)
        return int(self.sub[len(prefix):])


class EsiTokenError(Exception):
    """
    Raised when something goes wrong with tokens.
    """


def decode_access_token(access_token: str) -> DecodedAccessToken:
    """
    Converts an access token in JWT form to a :class:`sni.esi.sso.DecodedAccessToken`
    """
    document = jwt.decode(access_token, verify=False)
    if isinstance(document['scp'], str):
        document['scp'] = [document['scp']]
    try:
        return DecodedAccessToken(**document)
    except ValidationError as error:
        logging.error('Failed to decode access token: %s', str(error))
    raise EsiTokenError


def get_auth_url(esi_scopes: List[str],
                 state: str = '00000000-0000-0000-0000-000000000000') -> str:
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


def get_access_token_from_callback_code(
        code: str) -> AuthorizationCodeResponse:
    """
    Gets an access token (along with its refresh token) from an EVE SSO
    authorization code.

    See also:
        :class:`sni.esi.sso.AuthorizationCodeResponse`

    Returns:
        The document issued by the ESI, or ``None``

    Reference:
        `OAuth 2.0 for Web Based Applications <https://docs.esi.evetech.net/docs/sso/web_based_sso_flow.html>`

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
    try:
        response.raise_for_status()
        return AuthorizationCodeResponse(**response.json())
    except HTTPError as error:
        logging.error('Failed to get access token: %s', str(error))
    except ValidationError as error:
        logging.error('Failed to parse authorization code response: %s',
                      str(error))
    raise EsiTokenError


def refresh_access_token(refresh_token: str) -> AuthorizationCodeResponse:
    """
    Refreshes an access token.

    Returns:
        The response in an :class:`sni.esi.sso.AuthorizationCodeResponse`

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
    try:
        response.raise_for_status()
        return AuthorizationCodeResponse(**response.json())
    except HTTPError as error:
        logging.error('Failed to refresh access token: %s', str(error))
    except ValidationError as error:
        logging.error('Failed to parse authorization code response: %s',
                      str(error))
    raise EsiTokenError
