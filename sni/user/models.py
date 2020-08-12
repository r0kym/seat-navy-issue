"""
Models
"""

from typing import Iterator, List, Optional, Set

import mongoengine as me

from sni.esi.scope import EsiScope
import sni.utils as utils


class Alliance(me.Document):
    """
    EVE alliance database model.
    """

    SCHEMA_VERSION = 3
    """Latest schema version for this collection"""

    _version = me.IntField(default=SCHEMA_VERSION)
    """Schema version of this document"""

    alliance_id = me.IntField(unique=True)
    """Alliance id (according to the ESI)"""

    alliance_name = me.StringField(required=True)
    """Self explanatory"""

    authorized_to_login = me.BooleanField(default=None, null=True)
    """
    Wether the members of this alliance are allowed to login to SNI. See
    :meth:`sni.uac.uac.is_authorized_to_login`.
    """

    executor_corporation_id = me.IntField(required=True)
    """Id of the executor of this alliance"""

    mandatory_esi_scopes = me.ListField(
        me.StringField(choices=EsiScope), default=list
    )
    """Mandatory ESI scopes for the members of this alliance"""

    ticker = me.StringField(required=True)
    """Ticker of the alliance"""

    updated_on = me.DateTimeField(default=utils.now, required=True)
    """Timestamp of the last update of this document"""

    meta = {"indexes": ["alliance_id", "alliance_name",]}

    @property
    def ceo(self) -> "User":
        """
        Returns the ceo of the executor corporation.
        """
        return self.executor.ceo

    def coalitions(self) -> List["Coalition"]:
        """
        Returns the list of coalition this alliance is part of.

        Todo:
            Paginate the results
        """
        return list(Coalition.objects(member_alliances=self))

    def cumulated_mandatory_esi_scopes(self) -> Set[EsiScope]:
        """
        Returns the list (although it really is a set) of all the ESI scopes
        required by this alliance, and all the coalitions this alliance belongs
        to.
        """
        coalition_scopes = []
        for coalition in self.coalitions():
            coalition_scopes += coalition.mandatory_esi_scopes
        return set(self.mandatory_esi_scopes + coalition_scopes)

    @property
    def executor(self) -> "Corporation":
        """
        Returns the alliance's executor corporation as a
        :class:`sni.user.Corporation` object.
        """
        return Corporation.objects.get(
            corporation_id=self.executor_corporation_id
        )

    def users(self) -> List["User"]:
        """
        Return the member list of this alliance, according to the database.
        This may not be up to date with the ESI.
        """
        return list(self.user_iterator())

    def user_iterator(self) -> Iterator["User"]:
        """
        Returns an iterator over all the members of this alliance, according to
        the database. This may not be up to date with the ESI.
        """
        result = User.objects.aggregate(
            [
                {
                    "$lookup": {
                        "as": "corporation_data",
                        "foreignField": "_id",
                        "from": "corporation",
                        "localField": "corporation",
                    },
                },
                {"$unwind": "$corporation_data"},
                {
                    "$lookup": {
                        "as": "alliance_data",
                        "foreignField": "_id",
                        "from": "alliance",
                        "localField": "corporation_data.alliance",
                    },
                },
                {"$unwind": "$alliance_data"},
                {
                    "$match": {
                        "clearance_level": {"$gte": 0},
                        "alliance_data.alliance_id": self.alliance_id,
                    }
                },
                {
                    "$set": {
                        "character_name_lower": {"$toLower": "$character_name"}
                    }
                },
                {"$sort": {"character_name_lower": 1}},
                {"$project": {"_id": True}},
            ]
        )
        for item in result:
            yield User.objects(pk=item["_id"]).get()


class Corporation(me.Document):
    """
    EVE corporation database model.
    """

    SCHEMA_VERSION = 3
    """Latest schema version for this collection"""

    _version = me.IntField(default=SCHEMA_VERSION)
    """Schema version of this document"""

    authorized_to_login = me.BooleanField(default=None, null=True)
    """
    Wether the members of this corporation are allowed to login to SNI. See
    :meth:`sni.uac.uac.is_authorized_to_login`.
    """

    alliance = me.ReferenceField(
        Alliance, default=None, null=True, required=False
    )
    """Optional reference to the alliance this corporation belongs to"""

    ceo_character_id = me.IntField(required=True)
    """Character id (according to the ESI) of the CEO. See also :meth:`sni.user.models.Corporation.ceo`."""

    corporation_id = me.IntField(unique=True)
    """Id of the corporation (according to the ESI)"""

    corporation_name = me.StringField(required=True)
    """Name of the corporation"""

    mandatory_esi_scopes = me.ListField(
        me.StringField(choices=EsiScope), default=list
    )
    """Mandatory ESI scopes for the members of this corporation"""

    ticker = me.StringField(required=True)
    """Ticker of the corporation"""

    updated_on = me.DateTimeField(default=utils.now, required=True)
    """Timestamp of the last update of this document"""

    meta = {"indexes": ["corporation_id", "corporation_name",]}

    @property
    def ceo(self) -> "User":
        """
        Returns the corporation's ceo as a :class:`sni.user` object.
        """
        return User.objects.get(character_id=self.ceo_character_id)

    def coalitions(self) -> List["Coalition"]:
        """
        Returns the list of coalition this user is part of.
        """
        result: Set[Coalition] = set(
            Coalition.objects(member_corporations=self)
        )
        if self.alliance is not None:
            result.update(self.alliance.coalitions())
        return list(result)

    def cumulated_mandatory_esi_scopes(self) -> Set[EsiScope]:
        """
        Returns the list (although it really is a set) of all the ESI scopes
        required by this corporation, alliance, and all the coalitions this
        corporation is part of.
        """
        alliance_scopes = (
            self.alliance.mandatory_esi_scopes
            if self.alliance is not None
            else []
        )
        coalition_scopes = []
        for coalition in self.coalitions():
            coalition_scopes += coalition.mandatory_esi_scopes
        return set(
            self.mandatory_esi_scopes + alliance_scopes + coalition_scopes
        )

    def guests(self) -> List["User"]:
        """
        Return the guest list of this corporation, according to the database. A
        guest is a member with a clearance level of -1.
        """
        return list(self.guest_iterator())

    def guest_iterator(self) -> Iterator["User"]:
        """
        Returns an iterator over all the guests of this corporation, according
        to the database. A guest is a member with a clearance level of -1.
        """
        result = User.objects.aggregate(
            [
                {
                    "$lookup": {
                        "as": "corporation_data",
                        "foreignField": "_id",
                        "from": "corporation",
                        "localField": "corporation",
                    },
                },
                {"$unwind": "$corporation_data"},
                {
                    "$match": {
                        "clearance_level": {"$lt": 0},
                        "corporation_data.corporation_id": self.corporation_id,
                    }
                },
                {
                    "$set": {
                        "character_name_lower": {"$toLower": "$character_name"}
                    }
                },
                {"$sort": {"character_name_lower": 1}},
                {"$project": {"_id": True}},
            ]
        )
        for item in result:
            yield User.objects(pk=item["_id"]).get()

    def users(self) -> List["User"]:
        """
        Return the member list of this corporation, according to the database.
        This may not be up to date with the ESI.
        """
        return list(self.user_iterator())

    def user_iterator(self) -> Iterator["User"]:
        """
        Returns an iterator over all the members of this corporation, according
        to the database. This may not be up to date with the ESI.
        """
        result = User.objects.aggregate(
            [
                {
                    "$lookup": {
                        "as": "corporation_data",
                        "foreignField": "_id",
                        "from": "corporation",
                        "localField": "corporation",
                    },
                },
                {"$unwind": "$corporation_data"},
                {
                    "$match": {
                        "clearance_level": {"$gte": 0},
                        "corporation_data.corporation_id": self.corporation_id,
                    }
                },
                {
                    "$set": {
                        "character_name_lower": {"$toLower": "$character_name"}
                    }
                },
                {"$sort": {"character_name_lower": 1}},
                {"$project": {"_id": True}},
            ]
        )
        for item in result:
            yield User.objects(pk=item["_id"]).get()


class Coalition(me.Document):
    """
    EVE coalition. Coalitions are not formally represented in EVE, so they have
    to be created manually. An alliance can be part of multiple coalitions.
    """

    SCHEMA_VERSION = 6
    """Latest schema version for this collection"""

    _version = me.IntField(default=SCHEMA_VERSION)
    """Schema version of this document"""

    authorized_to_login = me.BooleanField(default=True, null=True)
    """
    Wether the members of this coalition are allowed to login to SNI. See
    :meth:`sni.uac.uac.is_authorized_to_login`.
    """

    created_on = me.DateTimeField(default=utils.now, required=True)
    """Timestamp of the creation of this document"""

    mandatory_esi_scopes = me.ListField(
        me.StringField(choices=EsiScope), default=list
    )
    """Mandatory ESI scopes for the members of this coalition"""

    member_alliances = me.ListField(me.ReferenceField(Alliance), default=list)
    """
    List of references to the member alliances (NOT users, for that, see
    :meth:`sni.user.models.Coalition.users` and
    :meth:`sni.user.models.Coalition.user_iterator`.
    """

    member_corporations = me.ListField(
        me.ReferenceField(Corporation), default=list
    )
    """
    Corporations that are direct members of this coalition (i.e. not through an
    alliance)
    """

    coalition_name = me.StringField(required=True, unique=True)
    """Name of the coalition"""

    ticker = me.StringField(default=str)
    """Ticker of the coalition"""

    updated_on = me.DateTimeField(default=utils.now, required=True)
    """Timestamp of the last update of this document"""

    meta = {"indexes": ["coalition_name",]}

    def users(self) -> List["User"]:
        """
        Return the member list of this coalition.
        """
        return list(self.user_iterator())

    def user_iterator(self) -> Iterator["User"]:
        """
        Returns an iterator over all the members of this coalition.
        """
        alliance_ids = [alliance.pk for alliance in self.member_alliances]
        corporation_ids = [
            corporation.pk for corporation in self.member_corporations
        ]
        result = User.objects.aggregate(
            [
                {
                    "$lookup": {
                        "as": "corporation_data",
                        "foreignField": "_id",
                        "from": "corporation",
                        "localField": "corporation",
                    },
                },
                {"$unwind": "$corporation_data"},
                {
                    "$lookup": {
                        "as": "alliance_data",
                        "foreignField": "_id",
                        "from": "alliance",
                        "localField": "corporation_data.alliance",
                    },
                },
                {"$unwind": "$alliance_data"},
                {
                    "$match": {
                        "$or": [
                            {"alliance_data._id": {"$in": alliance_ids}},
                            {"corporation_data._id": {"$in": corporation_ids}},
                        ],
                        "clearance_level": {"$gte": 0},
                    }
                },
                {
                    "$set": {
                        "character_name_lower": {"$toLower": "$character_name"}
                    }
                },
                {"$sort": {"character_name_lower": 1}},
                {"$project": {"_id": True}},
            ]
        )
        for item in result:
            yield User.objects(pk=item["_id"]).get()


class Group(me.Document):
    """
    Group model. A group is simply a collection of users.
    """

    SCHEMA_VERSION = 4
    """Latest schema version for this collection"""

    _version = me.IntField(default=SCHEMA_VERSION)
    """Schema version of this document"""

    authorized_to_login = me.BooleanField(default=None, null=True)
    """Wether the members of this alliance are allowed to login to SNI. See :meth:`sni.uac.uac.is_authorized_to_login`."""

    created_on = me.DateTimeField(default=utils.now, required=True)
    """Timestamp of the creation of this document"""

    discord_role_id = me.IntField(null=True)
    """Id of the corresponding discord role"""

    description = me.StringField(default=str)
    """Self explanatory"""

    is_autogroup = me.BooleanField(default=False, required=True)
    """Wether this group was created automatically by SNI (e.g. group of a corporation)"""

    map_to_discord = me.BooleanField(default=True, required=True)
    """Wether this group should be mapped as a Discord role"""

    map_to_teamspeak = me.BooleanField(default=True, required=True)
    """Wether this group should be mapped as a Teamspeak group"""

    members = me.ListField(me.ReferenceField("User"), default=list)
    """Member list"""

    group_name = me.StringField(required=True, unique=True)
    """Name of the group"""

    owner = me.ReferenceField("User", null=True)
    """Owner of the group. Can be ``None``."""

    teamspeak_sgid = me.IntField(null=True)
    """Teamspeak group id, if applicable"""

    updated_on = me.DateTimeField(default=utils.now, required=True)
    """Timestamp of the last update of this document"""

    meta = {"indexes": ["group_name",]}


class User(me.Document):
    """
    User model.

    A user corresponds to a single EVE character.
    """

    SCHEMA_VERSION = 3
    """Latest schema version for this collection"""

    _version = me.IntField(default=SCHEMA_VERSION)
    """Schema version of this document"""

    authorized_to_login = me.BooleanField(default=None, null=True)
    """Wether the members of this alliance are allowed to login to SNI. See :meth:`sni.uac.uac.is_authorized_to_login`."""

    character_id = me.IntField(unique=True)
    """Character id (according to the ESI)"""

    character_name = me.StringField(required=True)
    """Character name"""

    clearance_level = me.IntField(default=0, required=True)
    """Clearance level of this user. See :mod:`sni.uac.clearance`."""

    corporation = me.ReferenceField(Corporation, default=None, null=True)
    """Corporation this character belongs to, if applicable"""

    created_on = me.DateTimeField(default=utils.now, required=True)
    """Timestamp of the creation of this document"""

    discord_user_id = me.IntField(default=None, null=True)
    """Discord user id associated to this user, if applicable"""

    teamspeak_cldbid = me.IntField(default=None, null=True)
    """Teamspeak user id associated to this user, if applicable"""

    updated_on = me.DateTimeField(default=utils.now, required=True)
    """Timestamp of the last update of this document"""

    meta = {"indexes": ["character_id", "character_name",]}

    @property
    def alliance(self) -> Optional[Alliance]:
        """
        Returns the alliance the user is part of, if any
        """
        if self.corporation is not None:
            return self.corporation.alliance
        return None

    def cumulated_mandatory_esi_scopes(self) -> Set[EsiScope]:
        """
        Returns the list (although it really is a set) of all the ESI scopes
        required by the corporation, alliance, and all the coalitions the user
        is part of.
        """
        if self.corporation is not None:
            return self.corporation.cumulated_mandatory_esi_scopes()
        return set()

    def coalitions(self) -> List[Coalition]:
        """
        Returns the list of coalition this user is part of.
        """
        if self.corporation is not None:
            return self.corporation.coalitions()
        return []

    def is_ceo_of_alliance(self) -> bool:
        """
        Tells wether the user is the ceo of its corporation.
        """
        return (
            self.is_ceo_of_corporation()
            and self.corporation.alliance is not None
            and self.corporation.alliance.executor_corporation_id
            == self.corporation.corporation_id
        )

    def is_ceo_of_corporation(self) -> bool:
        """
        Tells wether the user is the ceo of its corporation.
        """
        return (
            self.corporation is not None
            and self.corporation.ceo_character_id == self.character_id
        )

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
            return f"[{ticker}] {self.character_name}"
        return self.character_name
