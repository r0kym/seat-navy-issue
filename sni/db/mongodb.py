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

import sni.conf as conf


def init():
    """
    Connects to the MongoDB instance.

    Does not return anything. Any call to ``mongoengine`` will act on that
    connection. It's magic.
    """
    logging.info('Connecting to database %s:%s', conf.get('database.host'),
                 conf.get('database.port'))
    me.connect(
        conf.get('database.database'),
        authentication_source=conf.get('database.authentication_source'),
        host=conf.get('database.host'),
        password=conf.get('database.password'),
        port=conf.get('database.port'),
        username=conf.get('database.username'),
    )


def get_pymongo_collection(
    collection_name: str,
    client: Optional[pymongo.MongoClient] = None
) -> pymongo.collection.Collection:
    """
    Returns a pymongo collection handler.
    """
    if client is None:
        client = new_pymongo_client()
    return client[conf.get('database.database')][collection_name]


def new_pymongo_client() -> pymongo.MongoClient:
    """
    Connects to the MongoDB database using pymongo and returns a client object.

    See also:
        `pymongo.mongo_client.MongoClient documentation
        <https://pymongo.readthedocs.io/en/stable/api/pymongo/mongo_client.html#pymongo.mongo_client.MongoClient>`_
    """
    authentication_database = conf.get('database.authentication_source')
    host = conf.get('database.host')
    password = quote_plus(conf.get('database.password'))
    port = conf.get('database.port')
    username = quote_plus(conf.get('database.username'))
    uri = f'mongodb://{username}:{password}@{host}:{port}/' + \
        f'?authSource={authentication_database}'
    return pymongo.MongoClient(uri)
