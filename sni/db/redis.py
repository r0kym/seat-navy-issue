"""
Redis related module
"""

import redis

import sni.conf as conf


def new_connection() -> redis.Redis:
    """
    Returns a new redis connection handler
    """
    return redis.Redis(
        db=conf.get('redis.database'),
        host=conf.get('redis.host'),
        port=conf.get('redis.port'),
    )
