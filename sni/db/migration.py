"""
Database migration utilities
"""

import logging
from typing import Any, Dict, Optional

from pymongo.collection import Collection

from .mongodb import get_pymongo_collection


def ensure_minimum_version(collection: Collection, version: int) -> None:
    """
    For all documents in the collection, if its ``_version`` field is less than
    the given version, sets it to that version.
    """
    collection.update_many(
        {"_version": {"$lt": version}}, {"$set": {"_version": version}},
    )


def finalize_migration(mongoengine_model_class) -> None:
    """
    Finalizes the migration process for a collection.

    Example::

        collection = start_migration(EsiRefreshToken)
        if collection is None:
            return
        ...
        finalize_migration(EsiRefreshToken)
    """
    mongoengine_model_class.ensure_indexes()


def has_outdated_documents(
    collection: Collection, schema_version: int
) -> bool:
    """
    Tells wether a (pymongo) collection has documents whose ``_version`` field
    have value less than the given schema version.
    """
    return (
        collection.count_documents({"_version": {"$ne": schema_version}}) > 0
    )


def set_if_not_exist(
    collection: Collection,
    field_name: str,
    value: Any,
    *,
    version: Optional[int] = None,
) -> None:
    """
    Creates a field with a given value in all documents, if that field does not
    already exist. If the version kwargs if specified, only update documents of
    that version.
    """
    query: Dict[str, Any] = {field_name: {"$exists": False}}
    if version is not None:
        query["_version"] = version
    update = {"$set": {field_name: value}}
    collection.update_many(query, update)


def start_migration(mongoengine_model_class) -> Optional[Collection]:
    """
    Starts the migration of a collection. If the returned value is ``None``,
    then the collection is up to date.

    Example::

        collection = start_migration(EsiRefreshToken)
        if collection is None:
            return
        ...
        finalize_migration(EsiRefreshToken)

    """
    # pylint: disable=protected-access
    collection_name = mongoengine_model_class._get_collection_name()
    collection = get_pymongo_collection(collection_name)
    if not has_outdated_documents(
        collection, mongoengine_model_class.SCHEMA_VERSION
    ):
        return None
    logging.info(
        'Migrating collection "%s" to version %d',
        collection_name,
        mongoengine_model_class.SCHEMA_VERSION,
    )
    collection.drop_indexes()
    return collection
