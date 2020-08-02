"""
Database models
"""

import mongoengine as me

from sni.user.models import User
import sni.utils as utils


class DiscordAuthenticationChallenge(me.Document):
    """
    Represents a pending authentication challenge.
    """

    code = me.StringField(required=True, unique=True)
    """Challenge code"""

    created_on = me.DateTimeField(default=utils.now, required=True)
    """Timestamp of the creation of this document"""

    user = me.ReferenceField(User, required=True, unique=True)
    """User that stated this authentication challenge"""

    meta = {
        "indexes": [{"fields": ["created_on"], "expireAfterSeconds": 120},],
    }
