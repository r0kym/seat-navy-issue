"""
User (aka character), corporation, and alliance management
"""

from typing import Iterator, List

import mongoengine as me

import sni.esi.esi as esi
import sni.time as time


class Alliance(me.Document):
    """
    EVE alliance database model.
    """
    alliance_id = me.IntField(unique=True)
    executor_corporation_id = me.IntField(required=True)
    alliance_name = me.StringField(required=True)
    ticker = me.StringField(required=True)
    updated_on = me.DateTimeField(default=time.now, required=True)

    def coalitions(self) -> List['Coalition']:
        """
        Returns the list of coalition this alliance is part of.

        Todo:
            Paginate the results
        """
        return list(Coalition.objects(members=self))

    @property
    def executor(self) -> 'Corporation':
        """
        Returns the alliance's executor corporation as a
        :class:`sni.user.user.Corporation` object.
        """
        return Corporation.objects.get(
            corporation_id=self.executor_corporation_id)

    def users(self) -> List['User']:
        """
        Return the member list of this alliance.
        """
        return list(self.user_iterator())

    def user_iterator(self) -> Iterator['User']:
        """
        Returns an iterator over all the members of this alliance.
        """
        for corporation in Corporation.objects(alliance=self):
            for usr in corporation.user_iterator():
                yield usr


class Coalition(me.Document):
    """
    EVE coalition. Coalitions are not formally represented in EVE, so they have
    to be created manually. An alliance can be part of multiple coalitions.
    """
    created_on = me.DateTimeField(default=time.now, required=True)
    members = me.ListField(me.ReferenceField(Alliance), default=list)
    name = me.StringField(required=True, unique=True)
    ticker = me.StringField(default=str)
    updated_on = me.DateTimeField(default=time.now, required=True)

    def users(self) -> List['User']:
        """
        Return the member list of this coalition.
        """
        return list(self.user_iterator())

    def user_iterator(self) -> Iterator['User']:
        """
        Returns an iterator over all the members of this coalition.
        """
        for alliance in self.members:
            for usr in alliance.user_iterator():
                yield usr


class Corporation(me.Document):
    """
    EVE corporation database model.
    """
    alliance = me.ReferenceField(Alliance,
                                 default=None,
                                 null=True,
                                 required=False)
    ceo_character_id = me.IntField(required=True)
    corporation_id = me.IntField(unique=True)
    corporation_name = me.StringField(required=True)
    ticker = me.StringField(required=True)
    updated_on = me.DateTimeField(default=time.now, required=True)

    @property
    def ceo(self) -> 'User':
        """
        Returns the corporation's ceo as a :class:`sni.user.user.User` object.
        """
        return User.objects.get(character_id=self.ceo_character_id)

    def users(self) -> List['User']:
        """
        Return the member list of this corporation.
        """
        return list(self.user_iterator())

    def user_iterator(self) -> Iterator['User']:
        """
        Returns an iterator over all the members of this corporation.
        """
        for usr in User.objects(corporation=self):
            yield usr


class User(me.Document):
    """
    User model.

    A user corresponds to a single EVE character.
    """
    character_id = me.IntField(unique=True)
    character_name = me.StringField(required=True)
    clearance_level = me.IntField(default=0, required=True)
    corporation = me.ReferenceField(Corporation, default=None, null=True)
    created_on = me.DateTimeField(default=time.now, required=True)
    teamspeak_cldbid = me.IntField()
    updated_on = me.DateTimeField(default=time.now, required=True)

    def is_ceo_of_alliance(self) -> bool:
        """
        Tells wether the user is the ceo of its corporation.
        """
        return (self.is_ceo_of_corporation()
                and self.corporation.alliance is not None
                and self.corporation.alliance.executor_corporation_id
                == self.corporation.corporation_id)

    def is_ceo_of_corporation(self) -> bool:
        """
        Tells wether the user is the ceo of its corporation.
        """
        return (self.corporation is not None
                and self.corporation.ceo_character_id == self.character_id)

    @property
    def tickered_name(self) -> str:
        """
        Returns the user's character name with its alliance ticker as a prefix.
        If the user is not in an alliance, then the corporation's ticker is
        used instead. If the user is not in any coproration (e.g. root), then
        there is no prefix.
        """
        ticker = None
        if self.corporation is not None:
            if self.corporation.alliance is not None:
                ticker = self.corporation.alliance.ticker
            else:
                ticker = self.corporation.ticker
        if ticker is not None:
            return f'[{ticker}] {self.character_name}'
        return self.character_name


def ensure_alliance(alliance_id: int) -> Alliance:
    """
    Ensures that an alliance exists, and returns it. It it does not, creates
    it by fetching relevant data from the ESI.

    Todo:
        Maintain alliance user group.
    """
    data = esi.get(f'latest/alliances/{alliance_id}').json()
    alliance = Alliance.objects(alliance_id=alliance_id).modify(
        new=True,
        set__alliance_id=alliance_id,
        set__alliance_name=data['name'],
        set__executor_corporation_id=int(data['executor_corporation_id']),
        set__ticker=data['ticker'],
        upsert=True,
    )
    # ensure_auto_group(data['name'])
    return alliance


def ensure_corporation(corporation_id: int) -> Corporation:
    """
    Ensures that a corporation exists, and returns it. It it does not, creates
    it by fetching relevant data from the ESI.

    Todo:
        Maintain corporation user group.
    """
    data = esi.get(f'latest/corporations/{corporation_id}').json()
    alliance = ensure_alliance(
        data['alliance_id']) if 'alliance_id' in data else None
    corporation = Corporation.objects(corporation_id=corporation_id).modify(
        new=True,
        set__alliance=alliance,
        set__ceo_character_id=int(data['ceo_id']),
        set__corporation_id=corporation_id,
        set__corporation_name=data['name'],
        set__ticker=data['ticker'],
        upsert=True,
    )
    # ensure_auto_group(data['name'])
    return corporation


def ensure_user(character_id: int) -> User:
    """
    Ensures that a user (with a valid ESI character ID) exists, and returns it.
    It it does not, creates it by fetching relevant data from the ESI. Also
    creates the character's corporation and alliance (if applicable).
    """
    usr: User = User.objects(character_id=character_id).first()
    if usr is None:
        data = esi.get(f'latest/characters/{character_id}').json()
        usr = User(
            character_id=character_id,
            character_name=data['name'],
            corporation=ensure_corporation(data['corporation_id']),
        ).save()
    return usr
