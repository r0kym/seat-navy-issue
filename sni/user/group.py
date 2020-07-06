"""
Group representation and utilities
"""

import logging
from typing import Any

import mongoengine as me
import mongoengine.signals as me_signals

import sni.scheduler as scheduler
import sni.utils as utils
import sni.user.user as user

GROUP_SCHEMA_VERSION = 3


class Group(me.Document):
    """
    Group model. A group is simply a collection of users.
    """
    _version = me.IntField(default=GROUP_SCHEMA_VERSION)
    created_on = me.DateTimeField(default=utils.now, required=True)
    discord_role_id = me.IntField(null=True)
    description = me.StringField(default=str)
    is_autogroup = me.BooleanField(default=False, required=True)
    map_to_discord = me.BooleanField(default=True, required=True)
    map_to_teamspeak = me.BooleanField(default=True, required=True)
    members = me.ListField(me.ReferenceField(user.User), required=True)
    group_name = me.StringField(required=True, unique=True)
    owner = me.ReferenceField(user.User, required=True)
    teamspeak_sgid = me.IntField(null=True)
    updated_on = me.DateTimeField(default=utils.now, required=True)


def ensure_autogroup(name: str) -> Group:
    """
    Ensured that an automatically created group exists. Automatic groups are
    owned by root.
    """
    grp = Group.objects(group_name=name).first()
    if grp is None:
        root = user.User.objects.get(character_id=0)
        grp = Group(
            is_autogroup=True,
            members=[root],
            group_name=name,
            owner=root,
        ).save()
    return grp


@me_signals.post_save.connect_via(user.User)
@scheduler.run_scheduled
def ensure_user_in_alliance_autogroup(_sender: Any, **kwargs):
    """
    Ensures that a user is in its alliance's autogroup.
    """
    usr: user.User = kwargs['document']
    if usr.corporation is None or usr.corporation.alliance is None:
        return
    grp = ensure_autogroup(usr.corporation.alliance.alliance_name)
    grp.modify(add_to_set__members=usr)
    logging.debug('Ensured user %s is in alliance autogroup %s',
                  usr.character_name, grp.group_name)


@me_signals.post_save.connect_via(user.User)
@scheduler.run_scheduled
def ensure_user_in_coalition_autogroups(_sender: Any, **kwargs):
    """
    Ensures that a user is in all its alliance's coalitions autogroups.
    """
    usr: user.User = kwargs['document']
    if usr.corporation is None or usr.corporation.alliance is None:
        return
    for coalition in usr.corporation.alliance.coalitions():
        grp = ensure_autogroup(coalition.coalition_name)
        grp.modify(add_to_set__members=usr)
        logging.debug('Ensured user %s is in coalition autogroup %s',
                      usr.character_name, grp.group_name)


@me_signals.post_save.connect_via(user.User)
@scheduler.run_scheduled
def ensure_user_in_corporation_autogroup(_sender: Any, **kwargs):
    """
    Ensures that a user is in its corporation's autogroup.
    """
    usr: user.User = kwargs['document']
    if usr.corporation is None:
        return
    grp = ensure_autogroup(usr.corporation.corporation_name)
    grp.modify(add_to_set__members=usr)
    logging.debug('Ensured user %s is in corporation autogroup %s',
                  usr.character_name, grp.group_name)
