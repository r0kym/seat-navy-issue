"""
Database layer

Reference:
    `MongoEngine User Documentation <http://docs.org/index.html>`_
"""

import logging
from typing import Callable, List

from mongoengine import connect

import sni.conf as conf
import sni.time as time
import sni.uac.token as token
import sni.uac.user as user


def init():
    """
    Connects to the MongoDB instance.

    Does not return anything. Any call to ``mongoengine`` will act on that
    connection. It's magic.
    """
    logging.info('Connecting to database %s:%s', conf.get('database.host'),
                 conf.get('database.port'))
    connect(
        conf.get('database.database'),
        authentication_source=conf.get('database.authentication_source'),
        host=conf.get('database.host'),
        password=conf.get('database.password'),
        port=conf.get('database.port'),
        username=conf.get('database.username'),
    )


def migrate() -> None:
    """
    Runs various migration jobs on the database.

    Should be called immediately after initializing the connection.
    """
    migration_tasks: List[Callable[[], None]] = [
        migrate_ensure_root,
        migrate_ensure_root_per_token,
        migrate_ensure_root_dyn_token,
    ]
    for task in migration_tasks:
        logging.info('Running database migration task %s', task.__name__)
        task()


def migrate_ensure_root() -> None:
    """
    Create root user if it does not exist.
    """
    if user.User.objects(character_id=0).count() == 0:
        root = user.User(
            character_id=0,
            character_name='root',
            created_on=time.now(),
        )
        root.save()
        logging.info('Created root user')


def migrate_ensure_root_per_token() -> None:
    """
    Create a permanent app token owned by root, if none exist.
    """
    root = user.get_user(character_id=0)
    if token.Token.objects(owner=root,
                           token_type=token.Token.TokenType.per).count() > 0:
        return
    root_per_token = token.create_permanent_app_token(root,
                                                      comments='Primary token')
    logging.info('No permanent app token owned by root, created one: %r',
                 token.to_jwt(root_per_token))


def migrate_ensure_root_dyn_token() -> None:
    """
    Create a dynamic app token owned by root, if none exist.
    """
    root = user.get_user(character_id=0)
    if token.Token.objects(owner=root,
                           token_type=token.Token.TokenType.dyn).count() > 0:
        return
    root_dyn_token = token.create_dynamic_app_token(root,
                                                    comments='Primary token')
    logging.info('No dynamic app token owned by root, created one: %r',
                 token.to_jwt(root_dyn_token))
