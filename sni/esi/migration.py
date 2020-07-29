"""
Database migrations
"""

import logging

from sni.db.mongodb import get_pymongo_collection
from sni.db.migration import (
    ensure_minimum_version,
    has_outdated_documents,
    set_if_not_exist,
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
    # pylint: disable=protected-access
    collection = get_pymongo_collection(EsiAccessToken._get_collection_name())
    schema_version = EsiAccessToken.SCHEMA_VERSION
    if not has_outdated_documents(collection, schema_version):
        return
    logging.info(
        'Migrating collection "esi_refresh_token" to v%d', schema_version
    )
    collection.drop_indexes()

    # v0 to v1
    # Set _version field to 1
    set_if_not_exist(collection, "_version", 1)

    # v1 to v2
    # Sets the valid field to True
    collection.delete_many({"refresh_token": {"$exists": False}})
    ensure_minimum_version(collection, 2)

    # Finally
    EsiAccessToken.ensure_indexes()


def migrate_esi_refresh_token() -> None:
    """
    Run migration tasks on the ``esi_refresh_token`` connection.
    """
    # pylint: disable=protected-access
    collection = get_pymongo_collection(EsiRefreshToken._get_collection_name())
    schema_version = EsiRefreshToken.SCHEMA_VERSION
    if not has_outdated_documents(collection, schema_version):
        return
    logging.info(
        'Migrating collection "esi_refresh_token" to v%d', schema_version
    )
    collection.drop_indexes()

    # v0 to v1
    # Set _version field to 1
    set_if_not_exist(collection, "_version", 1)

    # v1 to v2
    # Sets the valid field to True
    set_if_not_exist(collection, "valid", True, version=1)
    ensure_minimum_version(collection, 2)

    # Finally
    EsiRefreshToken.ensure_indexes()
