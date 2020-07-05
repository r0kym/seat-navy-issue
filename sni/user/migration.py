"""
Migration methode for user related collections
"""
import logging

import mongoengine as me

import sni.db.mongodb as mongodb
import sni.utils as utils
import sni.user.user as user
import sni.user.group as group


def ensure_root() -> None:
    """
    Create root user if it does not exist.
    """
    if user.User.objects(character_id=0).count() == 0:
        user.User(
            character_id=0,
            character_name='root',
            clearance_level=10,
            created_on=utils.now(),
        ).save()
        logging.info('Created root user')


def ensure_superuser_group() -> None:
    """
    Create the ``superusers`` group and makes sure that root is the owner.
    """
    group_name = 'superusers'
    root = user.User.objects.get(character_id=0)
    try:
        superusers: group.Group = group.Group.objects.get(
            group_name=group_name)
        superusers.owner = root
        superusers.modify(add_to_set__members=root)
        superusers.save()
    except me.DoesNotExist:
        group.Group(
            description="Superuser group.",
            map_to_teamspeak=False,
            members=[root],
            group_name=group_name,
            owner=root,
        ).save()
        logging.info('Created "%s" group', group_name)


def migrate_coalition():
    """
    Migrate the coalition documents to the latest schema
    """
    # pylint: disable=protected-access
    coalition_collection = mongodb.get_pymongo_collection(
        user.Coalition._get_collection_name())

    if coalition_collection.count_documents(
        {'_version': {
            '$ne': user.COALITION_SCHEMA_VERSION
        }}) == 0:
        return

    coalition_collection.drop_indexes()

    # v0 to v1
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
    user.Coalition.ensure_indexes()


def migrate_group():
    """
    Migrate the group collection from 10 to v2.

    Renames the ``name`` field to ``group_name``
    """
    # pylint: disable=protected-access
    group_collection = mongodb.get_pymongo_collection(
        group.Group._get_collection_name())

    if group_collection.count_documents(
        {'_version': {
            '$ne': group.GROUP_SCHEMA_VERSION
        }}) == 0:
        return

    group_collection.drop_indexes()

    # v0 to v1
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

    # Finally
    group.Group.ensure_indexes()


def migrate_user():
    """
    Migrate the user documents to the latest schema
    """
    # pylint: disable=protected-access
    user_collection = mongodb.get_pymongo_collection(
        user.User._get_collection_name())

    if user_collection.count_documents(
        {'_version': {
            '$ne': user.USER_SCHEMA_VERSION
        }}) == 0:
        return

    user_collection.drop_indexes()

    # v0 to v1
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

    # Finally
    user.User.ensure_indexes()
