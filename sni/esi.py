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

import jwt
from pydantic import BaseModel, ValidationError
import requests

import sni.conf as conf
import sni.dbmodels as dbmodels
import sni.time as time


# pylint: disable=too-few-public-methods
class AuthorizationCodeResponse(BaseModel):
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


class DecodedAuthorizationCode(BaseModel):
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


def process_esi_callback(code: str, state: str) -> bool:
    """
    Processes a callback from the ESI.

    See also:
        :func:`sni.esi.get_access_token`

    Reference:
        `OAuth 2.0 for Web Based Applications <https://docs.esi.evetech.net/docs/sso/web_based_sso_flow.html>`_
    """
    esi_response = get_access_token(code)
    if not esi_response:
        logging.error('Could not obtain or validate access token from ESI')
        return False
    state_code: dbmodels.StateCode = dbmodels.StateCode.objects(
        uuid=state).first()
    if not state_code:
        logging.error('Unknown state code %s', state)
        return False
    jwt_json = jwt.decode(esi_response.access_token, verify=False)
    if isinstance(jwt_json['scp'], str):
        jwt_json['scp'] = [jwt_json['scp']]
    decoded_jwt = DecodedAuthorizationCode(**jwt_json)
    user = dbmodels.User.objects(character_id=decoded_jwt.character_id).first()
    if not user:
        user = dbmodels.User(
            character_id=decoded_jwt.character_id,
            character_name=decoded_jwt.name,
            created_on=time.now(),
        )
        user.save()
    esi_token = dbmodels.EsiToken(
        access_token=esi_response.access_token,
        app_token=state_code.app_token,
        created_on=time.now(),
        expires_on=time.from_timestamp(decoded_jwt.exp),
        owner=user,
        refresh_token=esi_response.refresh_token,
        scopes=decoded_jwt.scp,
    )
    esi_token.save()
    return True


def get_access_token(code: str) -> Optional[AuthorizationCodeResponse]:
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
    try:
        response = requests.post(
            'https://login.eveonline.com/v2/oauth/token',
            headers=headers,
            data=data,
        )
        return AuthorizationCodeResponse(**response.json())
    except requests.HTTPError as error:
        logging.error('ESI request failed: %s', str(error))
    except ValidationError as error:
        logging.error('Invalid response from ESI: %s', str(error))
    return None


def refresh_access_token(
        refresh_token: str) -> Optional[AuthorizationCodeResponse]:
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
    try:
        return AuthorizationCodeResponse(**response.json())
    except ValidationError as error:
        logging.error('Invalid response from ESI %s', str(error))
        return None
