"""
Models
"""

from typing import Iterator, List, Optional, Set

import mongoengine as me

import sni.utils as utils

ALLIANCE_SCHEMA_VERSION = 3
COALITION_SCHEMA_VERSION = 4
CORPORATION_SCHEMA_VERSION = 3
GROUP_SCHEMA_VERSION = 4
USER_SCHEMA_VERSION = 3


class Alliance(me.Document):
    """
    EVE alliance database model.
    """
    _version = me.IntField(default=ALLIANCE_SCHEMA_VERSION)
    alliance_id = me.IntField(unique=True)
    alliance_name = me.StringField(required=True)
    authorized_to_login = me.BooleanField(default=None, null=True)
    executor_corporation_id = me.IntField(required=True)
    mandatory_esi_scopes = me.ListField(me.StringField(), default=list)
    ticker = me.StringField(required=True)
    updated_on = me.DateTimeField(default=utils.now, required=True)

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
        :class:`sni.user.Corporation` object.
        """
        return Corporation.objects.get(
            corporation_id=self.executor_corporation_id)

    def users(self) -> List['User']:
        """
        Return the member list of this alliance, according to the database.
        This may not be up to date with the ESI.
        """
        return list(self.user_iterator())

    def user_iterator(self) -> Iterator['User']:
        """
        Returns an iterator over all the members of this alliance, according to
        the database. This may not be up to date with the ESI.
        """
        for corporation in Corporation.objects(alliance=self):
            for usr in corporation.user_iterator():
                yield usr


class Coalition(me.Document):
    """
    EVE coalition. Coalitions are not formally represented in EVE, so they have
    to be created manually. An alliance can be part of multiple coalitions.
    """
    _version = me.IntField(default=COALITION_SCHEMA_VERSION)
    authorized_to_login = me.BooleanField(default=True, null=True)
    created_on = me.DateTimeField(default=utils.now, required=True)
    mandatory_esi_scopes = me.ListField(me.StringField(), default=list)
    members = me.ListField(me.ReferenceField(Alliance), default=list)
    coalition_name = me.StringField(required=True, unique=True)
    ticker = me.StringField(default=str)
    updated_on = me.DateTimeField(default=utils.now, required=True)

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
    _version = me.IntField(default=CORPORATION_SCHEMA_VERSION)
    authorized_to_login = me.BooleanField(default=None, null=True)
    alliance = me.ReferenceField(Alliance,
                                 default=None,
                                 null=True,
                                 required=False)
    ceo_character_id = me.IntField(required=True)
    corporation_id = me.IntField(unique=True)
    corporation_name = me.StringField(required=True)
    mandatory_esi_scopes = me.ListField(me.StringField(), default=list)
    ticker = me.StringField(required=True)
    updated_on = me.DateTimeField(default=utils.now, required=True)

    @property
    def ceo(self) -> 'User':
        """
        Returns the corporation's ceo as a :class:`sni.user` object.
        """
        return User.objects.get(character_id=self.ceo_character_id)

    def users(self) -> List['User']:
        """
        Return the member list of this corporation, according to the database.
        This may not be up to date with the ESI.
        """
        return list(self.user_iterator())

    def user_iterator(self) -> Iterator['User']:
        """
        Returns an iterator over all the members of this corporation, according
        to the database. This may not be up to date with the ESI.
        """
        for usr in User.objects(corporation=self):
            yield usr


class Group(me.Document):
    """
    Group model. A group is simply a collection of users.
    """
    _version = me.IntField(default=GROUP_SCHEMA_VERSION)
    authorized_to_login = me.BooleanField(default=None, null=True)
    created_on = me.DateTimeField(default=utils.now, required=True)
    discord_role_id = me.IntField(null=True)
    description = me.StringField(default=str)
    is_autogroup = me.BooleanField(default=False, required=True)
    map_to_discord = me.BooleanField(default=True, required=True)
    map_to_teamspeak = me.BooleanField(default=True, required=True)
    members = me.ListField(me.ReferenceField('User'),
                           default=list,
                           required=True)
    group_name = me.StringField(required=True, unique=True)
    owner = me.ReferenceField('User', required=True)
    teamspeak_sgid = me.IntField(null=True)
    updated_on = me.DateTimeField(default=utils.now, required=True)


class User(me.Document):
    """
    User model.

    A user corresponds to a single EVE character.
    """
    _version = me.IntField(default=USER_SCHEMA_VERSION)
    authorized_to_login = me.BooleanField(default=None, null=True)
    character_id = me.IntField(unique=True)
    character_name = me.StringField(required=True)
    clearance_level = me.IntField(default=0, required=True)
    corporation = me.ReferenceField(Corporation, default=None, null=True)
    created_on = me.DateTimeField(default=utils.now, required=True)
    discord_user_id = me.IntField(default=None, null=True)
    teamspeak_cldbid = me.IntField(default=None, null=True)
    updated_on = me.DateTimeField(default=utils.now, required=True)

    @property
    def alliance(self) -> Optional[Alliance]:
        """
        Returns the alliance the user is part of, if any
        """
        if self.corporation is not None:
            return self.corporation.alliance
        return None

    def cumulated_mandatory_esi_scopes(self) -> Set[str]:
        """
        Returns the list (although it really is a set) of all the ESI scopes
        required by the corporation, alliance, and all the coalitions the user
        is part of.
        """
        corporation_scopes = (self.corporation.mandatory_esi_scopes
                              if self.corporation is not None else [])
        alliance_scopes = (self.alliance.mandatory_esi_scopes
                           if self.alliance is not None else [])
        coalition_scopes = []
        for coalition in self.coalitions():
            coalition_scopes += coalition.mandatory_esi_scopes
        return set(corporation_scopes + alliance_scopes + coalition_scopes)

    def coalitions(self) -> List[Coalition]:
        """
        Returns the list of coalition this user is part of.
        """
        if self.alliance is not None:
            return self.alliance.coalitions()
        return []

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
