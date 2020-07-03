"""
Group representation and utilities
"""

import logging
from typing import Any

import mongoengine as me
import mongoengine.signals as me_signals

import sni.scheduler as scheduler
import sni.time as time
import sni.user.user as user


class Group(me.Document):
    """
    Group model. A group is simply a collection of users.
    """
    created_on = me.DateTimeField(default=time.now, required=True)
    description = me.StringField(default=str)
    is_autogroup = me.BooleanField(default=False, required=True)
    map_to_teamspeak = me.BooleanField(default=True, required=True)
    members = me.ListField(me.ReferenceField(user.User), required=True)
    name = me.StringField(required=True, unique=True)
    owner = me.ReferenceField(user.User, required=True)
    teamspeak_sgid = me.IntField()
    updated_on = me.DateTimeField(default=time.now, required=True)


def ensure_autogroup(name: str) -> Group:
    """
    Ensured that an automatically created group exists. Automatic groups are
    owned by root.
    """
    grp = Group.objects(name=name).first()
    if grp is None:
        root = user.User.objects.get(character_id=0)
        grp = Group(
            is_autogroup=True,
            members=[root],
            name=name,
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
                  usr.character_name, grp.name)


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
        grp = ensure_autogroup(coalition.name)
        grp.modify(add_to_set__members=usr)
        logging.debug('Ensured user %s is in coalition autogroup %s',
                      usr.character_name, grp.name)


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
                  usr.character_name, grp.name)
