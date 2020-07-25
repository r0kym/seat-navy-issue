"""
EVE token (access and refresh) management
"""

from enum import Enum
import logging
from typing import List, Optional, Set

from sni.user.models import User
from sni.user.user import ensure_user
import sni.utils as utils

from .esi import (
    esi_request,
    EsiResponse,
    get_esi_path_scope,
)
from .models import EsiAccessToken, EsiRefreshToken
from .sso import (
    AuthorizationCodeResponse,
    decode_access_token,
    DecodedAccessToken,
    refresh_access_token,
)


class TrackingStatus(int, Enum):
    """
    Tracking status of a user, i.e. wether this user has a valid refresh token
    attached to it, or not.
    """
    HAS_NO_REFRESH_TOKEN = 0
    ONLY_HAS_INVALID_REFRESH_TOKEN = 1
    HAS_A_VALID_REFRESH_TOKEN = 2


def available_esi_scopes(usr: User) -> Set[str]:
    """
    Given a user, returns all the scopes for which SNI has a valid refresh
    token.
    """
    scopes: List[str] = []
    for refresh_token in EsiRefreshToken.objects(owner=usr):
        scopes += refresh_token.scopes
    return set(scopes)


def esi_delete_on_befalf_of(path: str, character_id: int,
                            **kwargs) -> EsiResponse:
    """
    Wrapper for :meth:`sni.esi.esi.esi_request_on_behalf_of` for DELETE
    requests.
    """
    return esi_request_on_behalf_of('delete', path, character_id, **kwargs)


def esi_get_on_befalf_of(path: str, character_id: int,
                         **kwargs) -> EsiResponse:
    """
    Wrapper for :meth:`sni.esi.esi.esi_request_on_behalf_of` for GET requests.
    """
    return esi_request_on_behalf_of('get', path, character_id, **kwargs)


def esi_post_on_befalf_of(path: str, character_id: int,
                          **kwargs) -> EsiResponse:
    """
    Wrapper for :meth:`sni.esi.esi.esi_request_on_behalf_of` for POST requests.
    """
    return esi_request_on_behalf_of('post', path, character_id, **kwargs)


def esi_put_on_befalf_of(path: str, character_id: int,
                         **kwargs) -> EsiResponse:
    """
    Wrapper for :meth:`sni.esi.esi.esi_request_on_behalf_of` for PUT requests.
    """
    return esi_request_on_behalf_of('put', path, character_id, **kwargs)


def esi_request_on_behalf_of(http_method: str, path: str, character_id: int,
                             **kwargs) -> EsiResponse:
    """
    Wrapper for :meth:`sni.esi.esi.esi_request_on_behalf_of` for GET requests.
    """
    esi_scope = get_esi_path_scope(path)
    token = get_access_token(character_id, esi_scope).access_token
    return esi_request(http_method, path, token, **kwargs)


def get_access_token(character_id: int,
                     scope: Optional[str] = None) -> EsiAccessToken:
    """
    Returns an access token, refreshes if needed

    Todo:
        Support multiple scopes.
    """
    owner: User = User.objects.get(character_id=character_id)
    esi_access_token: EsiAccessToken = EsiAccessToken.objects(
        owner=owner,
        scopes=scope,
        expires_on__gt=utils.now(),
    ).first()
    if not esi_access_token:
        esi_refresh_token: EsiRefreshToken = EsiRefreshToken.objects(
            owner=owner,
            scopes=scope,
        ).first()
        if not esi_refresh_token:
            logging.error(
                'Could not find refresh token for user %s with scope %s',
                owner.character_name, scope)
            raise LookupError
        esi_access_token = save_esi_tokens(
            refresh_access_token(esi_refresh_token.refresh_token))
    return esi_access_token


def has_esi_scope(usr: User, scope: str) -> bool:
    """
    Tells wether the user has a refresh token with the given scope.
    """
    return EsiRefreshToken.objects(owner=usr, scopes=scope).first() is not None


def save_esi_tokens(esi_response: AuthorizationCodeResponse) -> EsiAccessToken:
    """
    Saves the tokens contained in an SSO reponse into the database.

    Create the owner user if necessary.

    Returns:
        The new ESI access token.
    """
    decoded_access_token = decode_access_token(esi_response.access_token)
    owner = ensure_user(decoded_access_token.character_id)
    esi_refresh_token: EsiRefreshToken = EsiRefreshToken.objects(
        owner=owner,
        scopes__all=decoded_access_token.scp,
    ).first()
    if esi_refresh_token:
        esi_refresh_token.refresh_token = esi_response.refresh_token
        esi_refresh_token.save()
    else:
        EsiRefreshToken(
            owner=owner,
            refresh_token=esi_response.refresh_token,
            scopes=decoded_access_token.scp,
        ).save()
    return EsiAccessToken(
        access_token=esi_response.access_token,
        expires_on=utils.from_timestamp(decoded_access_token.exp),
        owner=owner,
        scopes=decoded_access_token.scp,
    ).save()


def token_has_enough_scopes(access_token: DecodedAccessToken,
                            usr: User) -> bool:
    """
    Tells wether the access token has all the cropes that are required for a
    given user.
    """
    return usr.cumulated_mandatory_esi_scopes() <= set(access_token.scp)


def tracking_status(usr: User) -> TrackingStatus:
    """
    Reports the tracking status of this user, see
    :class:`sni.esi.token.TrackingStatus`
    """
    query_set = EsiRefreshToken.objects(owner=usr)
    if query_set.count() == 0:
        return TrackingStatus.HAS_NO_REFRESH_TOKEN
    cumulated_mandatory_esi_scopes = usr.cumulated_mandatory_esi_scopes()
    for refresh_token in query_set:
        if cumulated_mandatory_esi_scopes <= set(refresh_token.scopes):
            return TrackingStatus.HAS_A_VALID_REFRESH_TOKEN
    return TrackingStatus.ONLY_HAS_INVALID_REFRESH_TOKEN
