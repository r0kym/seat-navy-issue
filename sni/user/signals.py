"""
ODM signal handlers
"""

import logging
from typing import Any

import mongoengine.signals as signals

from sni.scheduler import run_scheduled

from .user import ensure_autogroup
from .models import User


@signals.post_save.connect_via(User)
@run_scheduled
def ensure_user_in_alliance_autogroup(_sender: Any, **kwargs):
    """
    Ensures that a user is in its alliance's autogroup.
    """
    usr: User = kwargs['document']
    if usr.corporation is None or usr.corporation.alliance is None:
        return
    grp = ensure_autogroup(usr.corporation.alliance.alliance_name)
    grp.modify(add_to_set__members=usr)
    logging.debug('Ensured user %s is in alliance autogroup %s',
                  usr.character_name, grp.group_name)


@signals.post_save.connect_via(User)
@run_scheduled
def ensure_user_in_coalition_autogroups(_sender: Any, **kwargs):
    """
    Ensures that a user is in all its alliance's coalitions autogroups.
    """
    usr: User = kwargs['document']
    if usr.corporation is None or usr.corporation.alliance is None:
        return
    for coalition in usr.corporation.alliance.coalitions():
        grp = ensure_autogroup(coalition.coalition_name)
        grp.modify(add_to_set__members=usr)
        logging.debug('Ensured user %s is in coalition autogroup %s',
                      usr.character_name, grp.group_name)


@signals.post_save.connect_via(User)
@run_scheduled
def ensure_user_in_corporation_autogroup(_sender: Any, **kwargs):
    """
    Ensures that a user is in its corporation's autogroup.
    """
    usr: User = kwargs['document']
    if usr.corporation is None:
        return
    grp = ensure_autogroup(usr.corporation.corporation_name)
    grp.modify(add_to_set__members=usr)
    logging.debug('Ensured user %s is in corporation autogroup %s',
                  usr.character_name, grp.group_name)
