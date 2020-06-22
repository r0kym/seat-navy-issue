"""
User management
"""

import mongoengine as me

import sni.time as time


class User(me.Document):
    """
    User model.

    A user corresponds to a single EVE character. A user can reference other
    users as "sub characters".
    """
    character_id = me.IntField(unique=True)
    character_name = me.StringField(required=True)
    created_on = me.DateTimeField(required=True, default=time.now)
    subcharacter_ids = me.ListField(me.IntField(), default=[])
