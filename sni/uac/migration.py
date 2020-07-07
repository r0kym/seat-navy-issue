"""
UAC specific migrations
"""

import logging

from sni.user.models import User
import sni.uac.token as token


def ensure_root_per_token() -> None:
    """
    Create a permanent app token owned by root, if none exist.
    """
    root = User.objects.get(character_id=0)
    if token.Token.objects(owner=root,
                           token_type=token.Token.TokenType.per).count() > 0:
        return
    root_per_token = token.create_permanent_app_token(root,
                                                      comments='Primary token')
    logging.info('No permanent app token owned by root, created one: %r',
                 token.to_jwt(root_per_token))


def ensure_root_dyn_token() -> None:
    """
    Create a dynamic app token owned by root, if none exist.
    """
    root = User.objects.get(character_id=0)
    if token.Token.objects(owner=root,
                           token_type=token.Token.TokenType.dyn).count() > 0:
        return
    root_dyn_token = token.create_dynamic_app_token(root,
                                                    comments='Primary token')
    logging.info('No dynamic app token owned by root, created one: %r',
                 token.to_jwt(root_dyn_token))
