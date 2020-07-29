"""
Database migration utilities
"""

from typing import Any, Dict, Optional

from pymongo.collection import Collection


def ensure_minimum_version(collection: Collection, version: int) -> None:
    """
    For all documents in the collection, if its ``_version`` field is less than
    the given version, sets it to that version.
    """
    collection.update_many(
        {"_version": {"$lt": version}}, {"$set": {"_version": version}},
    )


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
