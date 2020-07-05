"""
Database layer

Reference:
    `MongoEngine User Documentation <http://docs.org/index.html>`_
"""

import logging
from typing import Any

import mongoengine as me
import mongoengine.signals as me_signals

import sni.conf as conf
import sni.utils as utils


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
    me_signals.pre_save.connect(on_pre_save)


def on_pre_save(_sender: Any, document: me.Document):
    """
    If the document has a `updated_on`, sets it to the current datetime.
    """
    if 'updated_on' in document:
        document.updated_on = utils.now()


init()
