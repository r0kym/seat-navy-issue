"""
Redis related module
"""

from redis import ConnectionPool, Redis

from sni.conf import CONFIGURATION as conf

connection_pool = ConnectionPool(
    db=conf.redis.database, host=conf.redis.host, port=conf.redis.port,
)


def new_redis_connection() -> Redis:
    """
    Returns a new redis connection handler
    """
    return Redis(connection_pool=connection_pool)
