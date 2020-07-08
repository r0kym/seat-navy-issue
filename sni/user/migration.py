"""
Migration methode for user related collections
"""
import logging

import mongoengine as me

from sni.db.mongodb import get_pymongo_collection
from sni.db.migration import (
    ensure_minimum_version,
    has_outdated_documents,
    set_if_not_exist,
)
import sni.utils as utils

from .models import (
    COALITION_SCHEMA_VERSION,
    Coalition,
    GROUP_SCHEMA_VERSION,
    Group,
    USER_SCHEMA_VERSION,
    User,
)


def ensure_root() -> None:
    """
    Create root user if it does not exist.
    """
    if User.objects(character_id=0).count() == 0:
        logging.info('Creating root user')
        User(
            character_id=0,
            character_name='root',
            clearance_level=10,
            created_on=utils.now(),
        ).save()


def ensure_superuser_group() -> None:
    """
    Ensure that the ``superusers`` group exists and makes sure that root is the
    owner.
    """
    group_name = 'superusers'
    root = User.objects.get(character_id=0)
    try:
        superusers: Group = Group.objects.get(group_name=group_name)
        superusers.owner = root
        superusers.modify(add_to_set__members=root)
        superusers.discord_role_id = None
        superusers.map_to_discord = None
        superusers.map_to_teamspeak = False
        superusers.teamspeak_sgid = False
        superusers.save()
    except me.DoesNotExist:
        logging.info('Creating superuser group')
        Group(
            description="Superuser group.",
            discord_role_id=None,
            group_name=group_name,
            map_to_discord=None,
            map_to_teamspeak=False,
            members=[root],
            owner=root,
            teamspeak_sgid=False,
        ).save()


def migrate():
    """
    Migrates all schema
    """
    ensure_root()
    ensure_superuser_group()
    migrate_coalition()
    migrate_group()
    migrate_user()


def migrate_coalition():
    """
    Migrate the coalition documents to the latest schema
    """
    # pylint: disable=protected-access
    collection = get_pymongo_collection(Coalition._get_collection_name())

    if not has_outdated_documents(collection, COALITION_SCHEMA_VERSION):
        return

    logging.info('Migrating collection "coalition" to v%d',
                 COALITION_SCHEMA_VERSION)

    collection.drop_indexes()

    # v0 to v1
    # Set _version field to 1
    set_if_not_exist(collection, '_version', 1)

    # v1 to v2
    # Set name field to coalition_name
    collection.update_many(
        {'_version': 1},
        {
            '$rename': {
                'name': 'coalition_name'
            },
            '$set': {
                '_version': 2
            },
        },
    )

    # Finally
    Coalition.ensure_indexes()


def migrate_group():
    """
    Migrate the group collection from 10 to v2.

    Renames the ``name`` field to ``group_name``
    """
    # pylint: disable=protected-access
    collection = get_pymongo_collection(Group._get_collection_name())

    if not has_outdated_documents(collection, GROUP_SCHEMA_VERSION):
        return

    logging.info('Migrating collection "group" to v%d', GROUP_SCHEMA_VERSION)

    collection.drop_indexes()

    # v0 to v1
    # Set _version field to 1
    set_if_not_exist(collection, '_version', 1)

    # v1 to v2
    # Rename name field to group_name
    collection.update_many(
        {'_version': 1},
        {
            '$rename': {
                'name': 'group_name'
            },
            '$set': {
                '_version': 2
            },
        },
    )

    # v2 to v3
    # Ensures that
    # * discord_role_id exists (if not, sets it to None)
    # * teamspeak_sgid exists (if not, sets it to None)
    # * map_to_discord exists (if not, sets it to True)
    # * map_to_teamspeak exists (if not, sets it to True)
    collection.update_one(
        {
            '_version': 2,
            'group_name': 'superusers',
        },
        {
            '$set': {
                '_version': 3,
                'discord_role_id': None,
                'map_to_discord': False,
                'map_to_teamspeak': False,
                'teamspeak_sgid': None,
            },
        },
    )
    set_if_not_exist(collection, 'discord_role_id', None, version=2)
    set_if_not_exist(collection, 'teamspeak_sgid', None, version=2)
    set_if_not_exist(collection, 'map_to_discord', True, version=2)
    set_if_not_exist(collection, 'map_to_teamspeak', True, version=2)
    ensure_minimum_version(collection, 3)

    # Finally
    Group.ensure_indexes()


def migrate_user():
    """
    Migrate the user documents to the latest schema
    """
    # pylint: disable=protected-access
    collection = get_pymongo_collection(User._get_collection_name())

    if not has_outdated_documents(collection, USER_SCHEMA_VERSION):
        return

    logging.info('Migrating collection "user" to v%d', USER_SCHEMA_VERSION)

    collection.drop_indexes()

    # v0 to v1
    # Set _version field to 1
    set_if_not_exist(collection, '_version', 1)

    # v1 to v2
    # Add discord_user_id and teamspeak_cldbid fields, and set them to None
    set_if_not_exist(collection, 'discord_user_id', None, version=1)
    set_if_not_exist(collection, 'teamspeak_cldbid', None, version=1)
    ensure_minimum_version(collection, 2)

    # Finally
    User.ensure_indexes()
