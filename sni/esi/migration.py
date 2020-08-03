"""
Database migrations
"""


from sni.db.migration import (
    ensure_minimum_version,
    finalize_migration,
    set_if_not_exist,
    start_migration,
)

from .models import EsiAccessToken, EsiRefreshToken


def migrate() -> None:
    """
    Runs migration tasks
    """
    migrate_esi_access_token()
    migrate_esi_refresh_token()


def migrate_esi_access_token() -> None:
    """
    Run migration tasks on the ``esi_access_token`` connection.
    """
    collection = start_migration(EsiAccessToken)
    if collection is None:
        return

    # v0 to v1
    # Set _version field to 1
    set_if_not_exist(collection, "_version", 1)

    # v1 to v2
    # Sets the valid field to True
    collection.delete_many({"refresh_token": {"$exists": False}})
    ensure_minimum_version(collection, 2)

    # Finally
    finalize_migration(EsiAccessToken)


def migrate_esi_refresh_token() -> None:
    """
    Run migration tasks on the ``esi_refresh_token`` collection.
    """
    collection = start_migration(EsiRefreshToken)
    if collection is None:
        return

    # v0 to v1
    # Set _version field to 1
    set_if_not_exist(collection, "_version", 1)

    # v1 to v2
    # Sets the valid field to True
    set_if_not_exist(collection, "valid", True, version=1)
    ensure_minimum_version(collection, 2)

    # Finally
    finalize_migration(EsiRefreshToken)
