"""
User management
"""

import mongoengine as me

import sni.time as time
import sni.esi.esi as esi


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


def get_user(character_id: int) -> User:
    """
    Fetches a user from the database. If the user does not exist, it is
    created.
    """
    try:
        return User.objects.get(character_id=character_id)
    except me.DoesNotExist:
        user_data = esi.get(f'characters/{character_id}').json()
        return User(
            character_id=character_id,
            character_name=user_data['name'],
        )
