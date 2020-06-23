"""
User management
"""

import mongoengine as me

import sni.time as time
import sni.esi.esi as esi


class Alliance(me.Document):
    """
    EVE alliance database model.
    """
    alliance_id = me.IntField(unique=True)
    executor_corporation_id = me.IntField(required=True)
    alliance_name = me.StringField(required=True)
    ticker = me.StringField(required=True)

    @property
    def executor(self) -> 'Corporation':
        """
        Returns the alliance's executor corporation as a
        :class:`sni.uac.user.Corporation` object.
        """
        return Corporation.objects.get(
            corporation_id=self.executor_corporation_id)


class Corporation(me.Document):
    """
    EVE corporation database model.
    """
    alliance = me.ReferenceField(Alliance, required=False, default=None)
    ceo_character_id = me.IntField(required=True)
    corporation_id = me.IntField(unique=True)
    corporation_name = me.StringField(required=True)
    ticker = me.StringField(required=True)

    @property
    def ceo(self) -> 'User':
        """
        Returns the corporation's ceo as a :class:`sni.uac.user.User` object.
        """
        return User.ojects.get(character_id=self.ceo_character_id)


class User(me.Document):
    """
    User model.

    A user corresponds to a single EVE character. A user can reference other
    users as "sub characters".
    """
    character_id = me.IntField(unique=True)
    character_name = me.StringField(required=True)
    created_on = me.DateTimeField(required=True, default=time.now)
    corporation = me.ReferenceField(Corporation, default=None)


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


def ensure_alliance(alliance_id: int) -> Alliance:
    """
    Ensures that an alliance exists, and returns it. It it does not, creates
    it by fetching relevant data from the ESI.
    """
    try:
        return Alliance.objects.get(alliance_id=alliance_id)
    except me.DoesNotExist:
        data = esi.get(f'alliances/{alliance_id}').json()
        return Alliance(
            alliance_id=alliance_id,
            alliance_name=data['name'],
            executor_corporation_id=int(data['executor_corporation_id']),
            ticker=data['ticker'],
        ).save()


def ensure_corporation(corporation_id: int) -> Corporation:
    """
    Ensures that a corporation exists, and returns it. It it does not, creates
    it by fetching relevant data from the ESI.
    """
    try:
        return Corporation.objects.get(corporation_id=corporation_id)
    except me.DoesNotExist:
        data = esi.get(f'corporations/{corporation_id}').json()
        return Corporation(
            alliance=ensure_alliance(data['alliance_id']),
            ceo_character_id=int(data['ceo_id']),
            corporation_id=corporation_id,
            corporation_name=data['name'],
            ticker=data['ticker'],
        ).save()


def ensure_user(character_id: int) -> User:
    """
    Ensures that a user (with a valid ESI character ID) exists, and returns it.
    It it does not, creates it by fetching relevant data from the ESI.
    """
    try:
        return User.objects.get(character_id=character_id)
    except me.DoesNotExist:
        data = esi.get(f'characters/{character_id}').json()
        return User(
            character_id=character_id,
            character_name=data['name'],
            corporation=ensure_corporation(data['corporation_id']),
        ).save()
