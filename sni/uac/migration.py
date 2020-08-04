"""
UAC specific migrations
"""

import logging

from sni.user.models import User
from sni.db.migration import (
    ensure_minimum_version,
    finalize_migration,
    set_if_not_exist,
    start_migration,
)

import sni.uac.token as token
from .models import StateCode


def ensure_root_per_token() -> None:
    """
    Create a permanent app token owned by root, if none exist.
    """
    root = User.objects.get(character_id=0)
    if (
        token.Token.objects(
            owner=root, token_type=token.Token.TokenType.per
        ).count()
        > 0
    ):
        return
    root_per_token = token.create_permanent_app_token(
        root, comments="Primary token"
    )
    logging.info(
        "No permanent app token owned by root, created one: %r",
        token.to_jwt(root_per_token),
    )


def ensure_root_dyn_token() -> None:
    """
    Create a dynamic app token owned by root, if none exist.
    """
    root = User.objects.get(character_id=0)
    if (
        token.Token.objects(
            owner=root, token_type=token.Token.TokenType.dyn
        ).count()
        > 0
    ):
        return
    root_dyn_token = token.create_dynamic_app_token(
        root, comments="Primary token"
    )
    logging.info(
        "No dynamic app token owned by root, created one: %r",
        token.to_jwt(root_dyn_token),
    )


def migrate():
    """
    Migrates all schema and ensures basic documents
    """
    ensure_root_dyn_token()
    ensure_root_per_token()


def migrate_state_code():
    """
    Migrates the ``state_code`` collection
    """
    collection = start_migration(StateCode)
    if collection is None:
        return

    # v0 to v1
    # Set _version field to 1
    set_if_not_exist(collection, "_version", 1)

    # v1 to v2
    # Set inviting_corporation field to None
    set_if_not_exist(collection, "inviting_corporation", None, version=1)
    ensure_minimum_version(collection, 2)

    finalize_migration(StateCode)
