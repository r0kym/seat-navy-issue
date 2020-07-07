"""
Migration methode for user related collections
"""
import logging

import mongoengine as me

import sni.db.mongodb as mongodb
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
        User(
            character_id=0,
            character_name='root',
            clearance_level=10,
            created_on=utils.now(),
        ).save()
        logging.info('Created root user')


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
        logging.info('Created "%s" group', group_name)


def migrate_coalition():
    """
    Migrate the coalition documents to the latest schema
    """
    # pylint: disable=protected-access
    coalition_collection = mongodb.get_pymongo_collection(
        Coalition._get_collection_name())

    if coalition_collection.count_documents(
        {'_version': {
            '$ne': COALITION_SCHEMA_VERSION
        }}) == 0:
        return

    coalition_collection.drop_indexes()

    # v0 to v1
    # Set _version field to 1
    coalition_collection.update_many(
        {
            '_version': {
                '$exists': False
            },
        },
        {
            '$set': {
                '_version': 1
            },
        },
    )

    # v1 to v2
    # Set name field to coalition_name
    coalition_collection.update_many(
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
    group_collection = mongodb.get_pymongo_collection(
        Group._get_collection_name())

    if group_collection.count_documents(
        {'_version': {
            '$ne': GROUP_SCHEMA_VERSION
        }}) == 0:
        return

    group_collection.drop_indexes()

    # v0 to v1
    # Set _version field to 1
    group_collection.update_many(
        {
            '_version': {
                '$exists': False
            },
        },
        {
            '$set': {
                '_version': 1
            },
        },
    )

    # v1 to v2
    # Rename name field to group_name
    group_collection.update_many(
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
    group_collection.update_one(
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
    group_collection.update_many(
        {
            '_version': 2,
            'discord_role_id': {
                '$exists': False
            },
        },
        {
            '$set': {
                'discord_role_id': None
            },
        },
    )
    group_collection.update_many(
        {
            '_version': 2,
            'teamspeak_sgid': {
                '$exists': False
            },
        },
        {
            '$set': {
                'teamspeak_sgid': None
            },
        },
    )
    group_collection.update_many(
        {
            '_version': 2,
            'map_to_discord': {
                '$exists': False
            },
        },
        {
            '$set': {
                'map_to_discord': True
            },
        },
    )
    group_collection.update_many(
        {
            '_version': 2,
            'map_to_teamspeak': {
                '$exists': False
            },
        },
        {
            '$set': {
                'map_to_teamspeak': True
            },
        },
    )
    group_collection.update_many(
        {'_version': 2},
        {'$set': {
            '_version': 3
        }},
    )

    # Finally
    Group.ensure_indexes()


def migrate_user():
    """
    Migrate the user documents to the latest schema
    """
    # pylint: disable=protected-access
    user_collection = mongodb.get_pymongo_collection(
        User._get_collection_name())

    if user_collection.count_documents(
        {'_version': {
            '$ne': USER_SCHEMA_VERSION
        }}) == 0:
        return

    user_collection.drop_indexes()

    # v0 to v1
    # Set _version field to 1
    user_collection.update_many(
        {
            '_version': {
                '$exists': False
            },
        },
        {
            '$set': {
                '_version': 1
            },
        },
    )

    # v1 to v2
    # Add discord_user_id and teamspeak_cldbid fields, and set them to None
    user_collection.update_many(
        {'_version': 1},
        {
            '$set': {
                '_version': 2,
                'discord_user_id': None,
                'teamspeak_cldbid': None,
            },
        },
    )

    # Finally
    User.ensure_indexes()
