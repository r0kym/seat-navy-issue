"""
Redis related module
"""

from redis import ConnectionPool, Redis

import sni.conf as conf

connection_pool = ConnectionPool(
    db=conf.get('redis.database'),
    host=conf.get('redis.host'),
    port=conf.get('redis.port'),
)


def new_redis_connection() -> Redis:
    """
    Returns a new redis connection handler
    """
    return Redis(connection_pool=connection_pool)
