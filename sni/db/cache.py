"""
Redis based TTL cache
"""

from typing import Any, Optional
import logging
import pickle  # nosec

from redis.exceptions import RedisError
from xxhash import xxh64_hexdigest

from .redis import new_redis_connection

connection = new_redis_connection()


def cache_get(key: Any) -> Optional[Any]:
    """
    Retrieves a value from the cache, or returns None if the key is unknown.
    The key must be a picklable object.
    """
    hashed_key = hash_key(key)
    result = connection.get(hashed_key)
    if result is not None:
        logging.debug("Cache hit %s %s", hashed_key, str(key)[:20])
        return pickle.loads(result)  # nosec
    return None


def cache_set(key: Any, value: Any, ttl: int = 60) -> None:
    """
    Sets a value in the cache. The key and value must be picklable.
    """
    try:
        connection.setex(hash_key(key), ttl, pickle.dumps(value))
    except RedisError as error:
        logging.error("Redis error: %s", str(error))


def hash_key(document: Any) -> str:
    """
    Hashes a picklable object
    """
    return xxh64_hexdigest(pickle.dumps(document))


def invalidate_cache(key: Any):
    """
    Invalidates a cache value
    """
    connection.delete(hash_key(key))
