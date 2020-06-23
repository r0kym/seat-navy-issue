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


class Group(me.Document):
    """
    Group model. A group is simply a collection of users.
    """
    created_on = me.DateTimeField(required=True, default=time.now)
    description = me.StringField(default=str)
    members = me.ListField(me.ReferenceField(User), required=True)
    name = me.StringField(required=True, unique=True)
    owner = me.ReferenceField(User, required=True)
    updated_on = me.DateTimeField(required=True, default=time.now)


def create_group(owner: User, name: str, description: str = '') -> Group:
    """
    Creates a group. Sets the owner argument to be the owner as well as a
    member.
    """
    return Group(
        description=description,
        members=[owner],
        name=name,
        owner=owner,
    ).save()


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
