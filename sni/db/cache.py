"""
Redis based TTL cache
"""

import hashlib
import json

from typing import Any, Optional

from .redis import new_connection

connection = new_connection()


def cache_get(key: Any) -> Optional[Any]:
    """
    Retrieves a value from the cache, or returns None if the key is unknown.
    The key must be a JSON-dumpable variable.
    """
    result = connection.get(hash_key(key))
    if result is not None:
        return json.loads(result)
    return None


def cache_set(key: Any, value: Any, ttl: int = 60) -> None:
    """
    Sets a value in the cache. The key and value must be JSON-dumpable.
    """
    connection.setex(hash_key(key), ttl, json.dumps(value))


def hash_key(document: Any) -> str:
    """
    Hashes a JSON-dumpable variable
    """
    return hashlib.md5(json.dumps(document,
                                  sort_keys=True).encode()).hexdigest()


def invalidate_cache(key: Any):
    """
    Invalidates a cache value
    """
    connection.delete(hash_key(key))
