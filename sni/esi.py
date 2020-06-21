"""
EVE ESI module

This module is reponsible for talking to the EVE ESI.
"""

from base64 import urlsafe_b64encode
import logging
import re
from typing import List, Optional
from urllib.parse import urljoin

import jwt
import mongoengine
import pydantic
import requests

import sni.conf as conf
import sni.dbmodels as dbmodels

ESI_SWAGGER = 'https://esi.evetech.net/latest/swagger.json'


# pylint: disable=no-member
# pylint: disable=too-few-public-methods
class AuthorizationCodeResponse(pydantic.BaseModel):
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


# pylint: disable=no-member
class DecodedAccessToken(pydantic.BaseModel):
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


def decode_access_token(access_token: str) -> DecodedAccessToken:
    """
    Converts an access token in JWT form to a :class:`sni.esi.DecodedAccessToken`
    """
    document = jwt.decode(access_token, verify=False)
    if isinstance(document['scp'], str):
        document['scp'] = [document['scp']]
    return DecodedAccessToken(**document)


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


def get_access_token(code: str) -> AuthorizationCodeResponse:
    """
    Gets an access token (along with its refresh token) from an EVE SSO
    authorization code.

    See also:
        :class:`sni.esi.AuthorizationCodeResponse`

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
    return AuthorizationCodeResponse(**response.json())


def get_path_scope(path: str) -> Optional[str]:
    """
    Returns the ESI scope that is required for a given ESI path.

    Raises :class:`mongoengine.DoesNotExist` if no suitable path is found.

    Examples:

        >>> get_path_scope('latest/characters/0000000000/assets')
        'esi-assets.read_assets.v1'

        >>> get_path_scope('latest/alliances')
        None
    """
    esi_path: dbmodels.EsiPath
    for esi_path in dbmodels.EsiPath.objects:
        if re.search(esi_path.path_re, path):
            return esi_path.scope
    raise mongoengine.DoesNotExist


def load_esi_openapi() -> None:
    """
    Loads the ESI Swagger API into the database.

    Should be called in the initialization stage.

    See also:
        :class:`sni.dbmodels.EsiPath`
        `EVE Swagger Interface <https://esi.evetech.net/ui>`_
        `EVE Swagger Interface (JSON) <https://esi.evetech.net/latest/swagger.json>`_
    """
    logging.info('Loading ESI swagger specifications %s', ESI_SWAGGER)
    swagger = requests.get(ESI_SWAGGER).json()
    base_path = swagger['basePath'][1:]
    for path, path_data in swagger['paths'].items():
        for method, method_data in path_data.items():
            full_path = base_path + path
            path_re = '^' + re.sub(r'{\w+_id}', '[^/]+', full_path) + '?$'
            scope = None
            for security in method_data.get('security', []):
                scope = security.get('evesso', [scope])[0]
            dbmodels.EsiPath.objects(
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


def refresh_access_token(refresh_token: str) -> AuthorizationCodeResponse:
    """
    Refreshes an access token.

    Returns:
        The response in an :class:`sni.esi.AuthorizationCodeResponse`

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
    return AuthorizationCodeResponse(**response.json())
