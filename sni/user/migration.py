"""
Migration methode for user related collections
"""
import logging

from sni.db.mongodb import get_pymongo_collection
from sni.db.migration import (
    ensure_minimum_version,
    has_outdated_documents,
    set_if_not_exist,
)

from .models import (
    ALLIANCE_SCHEMA_VERSION,
    Alliance,
    COALITION_SCHEMA_VERSION,
    Coalition,
    CORPORATION_SCHEMA_VERSION,
    Corporation,
    GROUP_SCHEMA_VERSION,
    Group,
    USER_SCHEMA_VERSION,
    User,
)


def ensure_root() -> None:
    """
    Create root user if it does not exist.
    """
    User.objects(character_id=0).update(
        set__authorized_to_login=True,
        set__character_id=0,
        set__character_name='root',
        set__clearance_level=10,
        upsert=True,
    )


def ensure_superuser_group() -> None:
    """
    Ensure that the ``superusers`` group exists and makes sure that root is the
    owner.
    """
    root = User.objects.get(character_id=0)
    group_name = 'superusers'
    Group.objects(group_name='superusers').update(
        add_to_set__members=root,
        set__authorized_to_login=True,
        set__description="Superuser group",
        set__discord_role_id=None,
        set__is_autogroup=True,
        set__group_name=group_name,
        set__map_to_discord=False,
        set__map_to_teamspeak=False,
        set__owner=root,
        set__teamspeak_sgid=None,
        upsert=True,
    )


def migrate():
    """
    Migrates all schema
    """
    ensure_root()
    ensure_superuser_group()
    migrate_user()
    migrate_group()
    migrate_corporation()
    migrate_alliance()
    migrate_coalition()


def migrate_alliance():
    """
    Migrate the alliances documents to the latest schema
    """
    # pylint: disable=protected-access
    collection = get_pymongo_collection(Alliance._get_collection_name())

    if not has_outdated_documents(collection, ALLIANCE_SCHEMA_VERSION):
        return

    logging.info('Migrating collection "alliance" to v%d',
                 COALITION_SCHEMA_VERSION)

    collection.drop_indexes()

    # v0 to v1
    # Set _version field to 1
    set_if_not_exist(collection, '_version', 1)

    # v1 to v2
    # Set authorized_to_login field to None
    set_if_not_exist(collection, 'authorized_to_login', None, version=1)
    ensure_minimum_version(collection, 2)

    # Finally
    Alliance.ensure_indexes()


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

    # v2 to v3
    # Set authorized_to_login field to None
    set_if_not_exist(collection, 'authorized_to_login', None, version=2)
    ensure_minimum_version(collection, 3)

    # Finally
    Coalition.ensure_indexes()


def migrate_corporation():
    """
    Migrate the corporation documents to the latest schema
    """
    # pylint: disable=protected-access
    collection = get_pymongo_collection(Corporation._get_collection_name())

    if not has_outdated_documents(collection, CORPORATION_SCHEMA_VERSION):
        return

    logging.info('Migrating collection "corporation" to v%d',
                 CORPORATION_SCHEMA_VERSION)

    collection.drop_indexes()

    # v0 to v1
    # Set _version field to 1
    set_if_not_exist(collection, '_version', 1)

    # v1 to v2
    # Set authorized_to_login field to None
    set_if_not_exist(collection, 'authorized_to_login', None, version=1)
    ensure_minimum_version(collection, 2)

    # Finally
    Corporation.ensure_indexes()


def migrate_group():
    """
    Migrate the group documents to the latest schema
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

    # v3 to v4
    # Set authorized_to_login field to None
    set_if_not_exist(collection, 'authorized_to_login', None, version=3)
    ensure_minimum_version(collection, 4)

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

    # v2 to v3
    # Set authorized_to_login field to None
    set_if_not_exist(collection, 'authorized_to_login', None, version=2)
    ensure_minimum_version(collection, 3)

    # Finally
    User.ensure_indexes()
