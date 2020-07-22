"""
ODM signal handlers
"""

from typing import Any

import mongoengine.signals as signals

from sni.scheduler import scheduler

from .models import Coalition, User
from .jobs import (
    update_coalition_autogroup,
    update_user_autogroup,
)


@signals.post_save.connect_via(Coalition)
def on_coalition_post_save(_sender: Any, **kwargs):
    """
    Whenever a coalition is saved in the database.
    """
    if kwargs.get('created', False):
        coalition: Coalition = kwargs['document']
        scheduler.add_job(update_coalition_autogroup, args=(coalition, ))


@signals.post_save.connect_via(User)
def on_user_post_save(_sender: Any, **kwargs):
    """
    Whenever a user is saved in the database.
    """
    if not kwargs.get('created', False):
        usr: User = kwargs['document']
        if usr.character_id == 0:
            return
        # scheduler.add_job(update_user_from_esi, args=(usr, ))
        scheduler.add_job(update_user_autogroup, args=(usr, ))
