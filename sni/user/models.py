"""
Models
"""

from enum import Enum
from typing import Iterator, List, Optional, Set

import mongoengine as me

import sni.utils as utils


class EsiScope(str, Enum):
    """
    Enumeration of the ESI scopes
    """

    ESI_ALLIANCES_READ_CONTACTS_V1 = "esi-alliances.read_contacts.v1"
    ESI_ASSETS_READ_ASSETS_V1 = "esi-assets.read_assets.v1"
    ESI_ASSETS_READ_CORPORATION_ASSETS_V1 = (
        "esi-assets.read_corporation_assets.v1"
    )
    ESI_BOOKMARKS_READ_CHARACTER_BOOKMARKS_V1 = (
        "esi-bookmarks.read_character_bookmarks.v1"
    )
    ESI_BOOKMARKS_READ_CORPORATION_BOOKMARKS_V1 = (
        "esi-bookmarks.read_corporation_bookmarks.v1"
    )
    ESI_CALENDAR_READ_CALENDAR_EVENTS_V1 = (
        "esi-calendar.read_calendar_events.v1"
    )
    ESI_CALENDAR_RESPOND_CALENDAR_EVENTS_V1 = (
        "esi-calendar.respond_calendar_events.v1"
    )
    ESI_CHARACTERS_READ_AGENTS_RESEARCH_V1 = (
        "esi-characters.read_agents_research.v1"
    )
    ESI_CHARACTERS_READ_BLUEPRINTS_V1 = "esi-characters.read_blueprints.v1"
    ESI_CHARACTERS_READ_CHAT_CHANNELS_V1 = (
        "esi-characters.read_chat_channels.v1"
    )
    ESI_CHARACTERS_READ_CONTACTS_V1 = "esi-characters.read_contacts.v1"
    ESI_CHARACTERS_READ_CORPORATION_ROLES_V1 = (
        "esi-characters.read_corporation_roles.v1"
    )
    ESI_CHARACTERS_READ_FATIGUE_V1 = "esi-characters.read_fatigue.v1"
    ESI_CHARACTERS_READ_FW_STATS_V1 = "esi-characters.read_fw_stats.v1"
    ESI_CHARACTERS_READ_LOYALTY_V1 = "esi-characters.read_loyalty.v1"
    ESI_CHARACTERS_READ_MEDALS_V1 = "esi-characters.read_medals.v1"
    ESI_CHARACTERS_READ_NOTIFICATIONS_V1 = (
        "esi-characters.read_notifications.v1"
    )
    ESI_CHARACTERS_READ_OPPORTUNITIES_V1 = (
        "esi-characters.read_opportunities.v1"
    )
    ESI_CHARACTERS_READ_STANDINGS_V1 = "esi-characters.read_standings.v1"
    ESI_CHARACTERS_READ_TITLES_V1 = "esi-characters.read_titles.v1"
    ESI_CHARACTERS_WRITE_CONTACTS_V1 = "esi-characters.write_contacts.v1"
    ESI_CHARACTERSTATS_READ_V1 = "esi-characterstats.read.v1"
    ESI_CLONES_READ_CLONES_V1 = "esi-clones.read_clones.v1"
    ESI_CLONES_READ_IMPLANTS_V1 = "esi-clones.read_implants.v1"
    ESI_CONTRACTS_READ_CHARACTER_CONTRACTS_V1 = (
        "esi-contracts.read_character_contracts.v1"
    )
    ESI_CONTRACTS_READ_CORPORATION_CONTRACTS_V1 = (
        "esi-contracts.read_corporation_contracts.v1"
    )
    ESI_CORPORATIONS_READ_BLUEPRINTS_V1 = "esi-corporations.read_blueprints.v1"
    ESI_CORPORATIONS_READ_CONTACTS_V1 = "esi-corporations.read_contacts.v1"
    ESI_CORPORATIONS_READ_CONTAINER_LOGS_V1 = (
        "esi-corporations.read_container_logs.v1"
    )
    ESI_CORPORATIONS_READ_CORPORATION_MEMBERSHIP_V1 = (
        "esi-corporations.read_corporation_membership.v1"
    )
    ESI_CORPORATIONS_READ_DIVISIONS_V1 = "esi-corporations.read_divisions.v1"
    ESI_CORPORATIONS_READ_FACILITIES_V1 = "esi-corporations.read_facilities.v1"
    ESI_CORPORATIONS_READ_FW_STATS_V1 = "esi-corporations.read_fw_stats.v1"
    ESI_CORPORATIONS_READ_MEDALS_V1 = "esi-corporations.read_medals.v1"
    ESI_CORPORATIONS_READ_STANDINGS_V1 = "esi-corporations.read_standings.v1"
    ESI_CORPORATIONS_READ_STARBASES_V1 = "esi-corporations.read_starbases.v1"
    ESI_CORPORATIONS_READ_STRUCTURES_V1 = "esi-corporations.read_structures.v1"
    ESI_CORPORATIONS_READ_TITLES_V1 = "esi-corporations.read_titles.v1"
    ESI_CORPORATIONS_TRACK_MEMBERS_V1 = "esi-corporations.track_members.v1"
    ESI_FITTINGS_READ_FITTINGS_V1 = "esi-fittings.read_fittings.v1"
    ESI_FITTINGS_WRITE_FITTINGS_V1 = "esi-fittings.write_fittings.v1"
    ESI_FLEETS_READ_FLEET_V1 = "esi-fleets.read_fleet.v1"
    ESI_FLEETS_WRITE_FLEET_V1 = "esi-fleets.write_fleet.v1"
    ESI_INDUSTRY_READ_CHARACTER_JOBS_V1 = "esi-industry.read_character_jobs.v1"
    ESI_INDUSTRY_READ_CHARACTER_MINING_V1 = (
        "esi-industry.read_character_mining.v1"
    )
    ESI_INDUSTRY_READ_CORPORATION_JOBS_V1 = (
        "esi-industry.read_corporation_jobs.v1"
    )
    ESI_INDUSTRY_READ_CORPORATION_MINING_V1 = (
        "esi-industry.read_corporation_mining.v1"
    )
    ESI_KILLMAILS_READ_CORPORATION_KILLMAILS_V1 = (
        "esi-killmails.read_corporation_killmails.v1"
    )
    ESI_KILLMAILS_READ_KILLMAILS_V1 = "esi-killmails.read_killmails.v1"
    ESI_LOCATION_READ_LOCATION_V1 = "esi-location.read_location.v1"
    ESI_LOCATION_READ_ONLINE_V1 = "esi-location.read_online.v1"
    ESI_LOCATION_READ_SHIP_TYPE_V1 = "esi-location.read_ship_type.v1"
    ESI_MAIL_ORGANIZE_MAIL_V1 = "esi-mail.organize_mail.v1"
    ESI_MAIL_READ_MAIL_V1 = "esi-mail.read_mail.v1"
    ESI_MAIL_SEND_MAIL_V1 = "esi-mail.send_mail.v1"
    ESI_MARKETS_READ_CHARACTER_ORDERS_V1 = (
        "esi-markets.read_character_orders.v1"
    )
    ESI_MARKETS_READ_CORPORATION_ORDERS_V1 = (
        "esi-markets.read_corporation_orders.v1"
    )
    ESI_MARKETS_STRUCTURE_MARKETS_V1 = "esi-markets.structure_markets.v1"
    ESI_PLANETS_MANAGE_PLANETS_V1 = "esi-planets.manage_planets.v1"
    ESI_PLANETS_READ_CUSTOMS_OFFICES_V1 = "esi-planets.read_customs_offices.v1"
    ESI_SEARCH_SEARCH_STRUCTURES_V1 = "esi-search.search_structures.v1"
    ESI_SKILLS_READ_SKILLQUEUE_V1 = "esi-skills.read_skillqueue.v1"
    ESI_SKILLS_READ_SKILLS_V1 = "esi-skills.read_skills.v1"
    ESI_UI_OPEN_WINDOW_V1 = "esi-ui.open_window.v1"
    ESI_UI_WRITE_WAYPOINT_V1 = "esi-ui.write_waypoint.v1"
    ESI_UNIVERSE_READ_STRUCTURES_V1 = "esi-universe.read_structures.v1"
    ESI_WALLET_READ_CHARACTER_WALLET_V1 = "esi-wallet.read_character_wallet.v1"
    ESI_WALLET_READ_CORPORATION_WALLET_V1 = (
        "esi-wallet.read_corporation_wallet.v1"
    )
    ESI_WALLET_READ_CORPORATION_WALLETS_V1 = (
        "esi-wallet.read_corporation_wallets.v1"
    )
    PUBLICDATA = "publicData"


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
    """Wether the members of this alliance are allowed to login to SNI. See :meth:`sni.uac.uac.is_authorized_to_login`."""

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
        return list(Coalition.objects(members=self))

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


class Coalition(me.Document):
    """
    EVE coalition. Coalitions are not formally represented in EVE, so they have
    to be created manually. An alliance can be part of multiple coalitions.
    """

    SCHEMA_VERSION = 4
    """Latest schema version for this collection"""

    _version = me.IntField(default=SCHEMA_VERSION)
    """Schema version of this document"""

    authorized_to_login = me.BooleanField(default=True, null=True)
    """Wether the members of this alliance are allowed to login to SNI. See :meth:`sni.uac.uac.is_authorized_to_login`."""

    created_on = me.DateTimeField(default=utils.now, required=True)
    """Timestamp of the creation of this document"""

    mandatory_esi_scopes = me.ListField(
        me.StringField(choices=EsiScope), default=list
    )
    """Mandatory ESI scopes for the members of this coalition"""

    members = me.ListField(me.ReferenceField(Alliance), default=list)
    """List of references to the member alliances (NOT users, for that, see :meth:`sni.user.models.Coalition.users` and :meth:`sni.user.models.Coalition.user_iterator`."""

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
        members_ids = [alliance.pk for alliance in self.members]
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
                        "alliance_data._id": {"$in": members_ids},
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
    """Wether the members of this alliance are allowed to login to SNI. See :meth:`sni.uac.uac.is_authorized_to_login`."""

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

    def coalitions(self) -> List[Coalition]:
        """
        Returns the list of coalition this user is part of.
        """
        if self.alliance is not None:
            return self.alliance.coalitions()
        return []

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
