"""
EVE token (access and refresh) management
"""

import logging
from typing import List, Optional, Set

from sni.user.models import User
from sni.user.user import ensure_user
import sni.utils as utils

from .models import EsiAccessToken, EsiRefreshToken
from .sso import (
    AuthorizationCodeResponse,
    decode_access_token,
    refresh_access_token,
)


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


def available_esi_scopes(usr: User) -> Set[str]:
    """
    Given a user, returns all the scopes for which SNI has a valid refresh
    token.
    """
    scopes: List[str] = []
    for refresh_token in EsiRefreshToken.objects(owner=usr):
        scopes += refresh_token.scopes
    return set(scopes)
