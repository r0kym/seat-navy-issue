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


from .models import EsiCharacterLocation


def migrate() -> None:
    """
    Runs migration tasks
    """
    migrate_character_location()


def migrate_character_location() -> None:
    """
    Migrate the ``esi_character_location`` collection
    """
    # pylint: disable=protected-access
    collection = get_pymongo_collection(
        EsiCharacterLocation._get_collection_name()
    )

    if not has_outdated_documents(
        collection, EsiCharacterLocation.SCHEMA_VERSION
    ):
        return

    logging.info(
        'Migrating collection "esi_character_location" to v%d',
        EsiCharacterLocation.SCHEMA_VERSION,
    )

    collection.drop_indexes()

    # v0 to v1
    # Set _version field to 1
    set_if_not_exist(collection, "_version", 1)

    # v1 to v2
    # Set structure_name fields to None
    set_if_not_exist(collection, "structure_name", None, version=1)
    ensure_minimum_version(collection, 2)

    # Finally
    EsiCharacterLocation.ensure_indexes()
