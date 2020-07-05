"""
Migration methode for user related collections
"""
import logging

import mongoengine as me

import sni.utils as utils
import sni.user.user as user
import sni.user.group as group


def coalition_v0_to_v1():
    """
    Migrate the coalition collection from v0 to v1.

    Simply adds the ``_version`` field and sets it to ``1``.
    """
    user.Coalition.objects(_version__exists=False).update(set___version=1)


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
        superusers: group.Group = group.Group.objects.get(name=group_name)
        superusers.owner = root
        superusers.modify(add_to_set__members=root)
        superusers.save()
    except me.DoesNotExist:
        group.Group(
            description="Superuser group.",
            map_to_teamspeak=False,
            members=[root],
            name=group_name,
            owner=root,
        ).save()
        logging.info('Created "%s" group', group_name)

def group_v0_to_v1():
    """
    Migrate the group collection from v0 to v1.

    Simply adds the ``_version`` field and sets it to ``1``.
    """
    group.Group.objects(_version__exists=False).update(set___version=1)


def user_v0_to_v1():
    """
    Migrate the user collection from v0 to v1.

    Simply adds the ``_version`` field and sets it to ``1``.
    """
    user.User.objects(_version__exists=False).update(set___version=1)