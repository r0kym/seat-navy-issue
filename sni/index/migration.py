"""
Database migrations
"""

from sni.db.migration import (
    ensure_minimum_version,
    finalize_migration,
    set_if_not_exist,
    start_migration,
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
    collection = start_migration(EsiCharacterLocation)
    if collection is None:
        return

    # v0 to v1
    # Set _version field to 1
    set_if_not_exist(collection, "_version", 1)

    # v1 to v2
    # Set structure_name fields to None
    set_if_not_exist(collection, "structure_name", None, version=1)
    ensure_minimum_version(collection, 2)

    # Finally
    finalize_migration(EsiCharacterLocation)
