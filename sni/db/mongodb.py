"""
Database layer

Reference:
    `MongoEngine User Documentation <http://docs.org/index.html>`_
"""

import logging
from typing import Optional
from urllib.parse import quote_plus

import mongoengine as me
import pymongo
import pymongo.collection

from sni.conf import CONFIGURATION as conf


def init_mongodb():
    """
    Connects to the MongoDB instance.

    Does not return anything. Any call to ``mongoengine`` will act on that
    connection. It's magic.
    """
    logging.info(
        "Connecting to database %s:%s", conf.database.host, conf.database.port
    )
    me.connect(
        conf.database.database,
        authentication_source=conf.database.authentication_source,
        host=conf.database.host,
        password=conf.database.password.get_secret_value(),
        port=conf.database.port,
        username=conf.database.username,
    )


def get_pymongo_collection(
    collection_name: str, client: Optional[pymongo.MongoClient] = None
) -> pymongo.collection.Collection:
    """
    Returns a pymongo collection handler.
    """
    if client is None:
        client = new_pymongo_client()
    return client[conf.database.database][collection_name]


def new_pymongo_client() -> pymongo.MongoClient:
    """
    Connects to the MongoDB database using pymongo and returns a client object.

    See also:
        `pymongo.mongo_client.MongoClient documentation
        <https://pymongo.readthedocs.io/en/stable/api/pymongo/mongo_client.html#pymongo.mongo_client.MongoClient>`_
    """
    authentication_database = conf.database.authentication_source
    host = conf.database.host
    password = quote_plus(conf.database.password.get_secret_value())
    port = conf.database.port
    username = quote_plus(conf.database.username)
    uri = (
        f"mongodb://{username}:{password}@{host}:{port}/"
        + f"?authSource={authentication_database}"
    )
    return pymongo.MongoClient(uri)
