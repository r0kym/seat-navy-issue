"""
Clearance management and verification. Each user has a **clearance level**,
which is an integer:

* Level -1: User is a guest and has no priviledge whatsoever.

* Level 0: User only have access to public data and read-write access to its
  own ESI.

* Level 1: User has access to read-only ESI (i.e. ``GET`` calls) of all members
  of his corporation.

* Level 2: User has access to read-write ESI (i.e. all http methods) of all
  members of his corporation.

* Level 3: User has access to read-only ESI (i.e. ``GET`` calls) of all members
  of his alliance.

* Level 4: User has access to read-write ESI (i.e. all http methods) of all
  members of his alliance.

* Level 5: User has access to read-only ESI (i.e. ``GET`` calls) of all members
  of his coalition.

* Level 6: User has access to read-write ESI (i.e. all http methods) of all
  members of his coalition.

* Level 7: User has access to read-only ESI (i.e. ``GET`` calls) of all members
  regisered on this SNI instance.

* Level 8: User has access to read-write ESI (i.e. all http methods) of all
  members regisered on this SNI instance.

* Level 9: User has clearance level 8 and some administrative priviledges.

* Level 10: Superuser.

Furthermore, note that

* Any user can raise any other to its own clearance level, provided they are in
  the same corporation (for levels 1 and 2), alliance (for levels 3 and 4), or
  coalition (for levels 5 and 6).

* Demoting users is considered an administrative task and requires a clearance
  of at least 9.

* Clearance levels are public informations.

See :meth:`sni.uac.clearance.has_clearance` for a precise specification of how
clearance levels are checked, and :const:`sni.uac.clearance.SCOPE_LEVELS` for
the declaration of all scopes.
"""

from dataclasses import dataclass
import logging
from typing import Dict, Optional

from sni.esi.scope import EsiScope
from sni.db.cache import cache_get, cache_set
from sni.user.models import Coalition, User


class AbstractScope:
    """
    Represents an abstract scope. In SNI, a scope is a class that determines
    wether a *source* user is authorized to perform an action against a
    *target* user (see :meth:`sni.uac.clearance.AbstractScope.has_clearance`).
    """

    def has_clearance(self, source: User, target: Optional[User]) -> bool:
        """
        Pure virtual methode, raises a ``NotImplementedError``.
        """
        raise NotImplementedError


@dataclass
class AbsoluteScope(AbstractScope):
    """
    An absolute scope asserts that the source user has at least a pretermined
    clearance level.
    """

    level: int

    def has_clearance(self, source: User, target: Optional[User]) -> bool:
        if target is not None:
            logging.warning("Absolute scopes should not have targets")
        return self.level <= source.clearance_level


@dataclass
class ClearanceModificationScope(AbstractScope):
    """
    This scope determines when a user is authorized to change the clearance
    level of another user. See :meth:`sni.uac.clearance.ClearanceModificationScope.has_clearance`.
    """

    level: int

    def has_clearance(self, source: User, target: Optional[User]) -> bool:
        """
        For the source user to change the clearance level of the target user at
        the level indicated in
        :data:`sni.uac.clearance.ClearanceModificationScope.level`, the
        clearance level of the source must be hierarchically superior to the
        target, and have read-write access to the target's corporation,
        alliance, or coalition, whichever is most global. In addition, the
        source must have at least the same clearance level than the target.
        """
        if target is None:
            logging.warning("Clearance modification scopes must have a target")
            return False
        if source == target:  # Cannot change own clearance
            return False
        return source.clearance_level >= max(
            [
                distance_penalty(source, target) + 1,
                self.level,
                target.clearance_level,
            ]
        )


@dataclass
class ESIScope(AbstractScope):
    """
    This scope determines when a user is authorized to read or write ESI data.
    """

    level: int

    def has_clearance(self, source: User, target: Optional[User]) -> bool:
        if target is None:
            logging.warning("ESI scopes must have a target")
            return False
        if source.clearance_level >= 7:
            return True
        return (
            source.clearance_level
            >= distance_penalty(source, target) + self.level
        )


SCOPES: Dict[str, AbstractScope] = {
    EsiScope.ESI_ALLIANCES_READ_CONTACTS_V1: ESIScope(0),
    EsiScope.ESI_ASSETS_READ_ASSETS_V1: ESIScope(0),
    EsiScope.ESI_ASSETS_READ_CORPORATION_ASSETS_V1: ESIScope(0),
    EsiScope.ESI_BOOKMARKS_READ_CHARACTER_BOOKMARKS_V1: ESIScope(0),
    EsiScope.ESI_BOOKMARKS_READ_CORPORATION_BOOKMARKS_V1: ESIScope(0),
    EsiScope.ESI_CALENDAR_READ_CALENDAR_EVENTS_V1: ESIScope(0),
    EsiScope.ESI_CALENDAR_RESPOND_CALENDAR_EVENTS_V1: ESIScope(1),
    EsiScope.ESI_CHARACTERS_READ_AGENTS_RESEARCH_V1: ESIScope(0),
    EsiScope.ESI_CHARACTERS_READ_BLUEPRINTS_V1: ESIScope(0),
    EsiScope.ESI_CHARACTERS_READ_CHAT_CHANNELS_V1: ESIScope(0),
    EsiScope.ESI_CHARACTERS_READ_CONTACTS_V1: ESIScope(0),
    EsiScope.ESI_CHARACTERS_READ_CORPORATION_ROLES_V1: ESIScope(0),
    EsiScope.ESI_CHARACTERS_READ_FATIGUE_V1: ESIScope(0),
    EsiScope.ESI_CHARACTERS_READ_FW_STATS_V1: ESIScope(0),
    EsiScope.ESI_CHARACTERS_READ_LOYALTY_V1: ESIScope(0),
    EsiScope.ESI_CHARACTERS_READ_MEDALS_V1: ESIScope(0),
    EsiScope.ESI_CHARACTERS_READ_NOTIFICATIONS_V1: ESIScope(0),
    EsiScope.ESI_CHARACTERS_READ_OPPORTUNITIES_V1: ESIScope(0),
    EsiScope.ESI_CHARACTERS_READ_STANDINGS_V1: ESIScope(0),
    EsiScope.ESI_CHARACTERS_READ_TITLES_V1: ESIScope(0),
    EsiScope.ESI_CHARACTERS_WRITE_CONTACTS_V1: ESIScope(1),
    EsiScope.ESI_CHARACTERSTATS_READ_V1: ESIScope(0),
    EsiScope.ESI_CLONES_READ_CLONES_V1: ESIScope(0),
    EsiScope.ESI_CLONES_READ_IMPLANTS_V1: ESIScope(0),
    EsiScope.ESI_CONTRACTS_READ_CHARACTER_CONTRACTS_V1: ESIScope(0),
    EsiScope.ESI_CONTRACTS_READ_CORPORATION_CONTRACTS_V1: ESIScope(0),
    EsiScope.ESI_CORPORATIONS_READ_BLUEPRINTS_V1: ESIScope(0),
    EsiScope.ESI_CORPORATIONS_READ_CONTACTS_V1: ESIScope(0),
    EsiScope.ESI_CORPORATIONS_READ_CONTAINER_LOGS_V1: ESIScope(0),
    EsiScope.ESI_CORPORATIONS_READ_CORPORATION_MEMBERSHIP_V1: ESIScope(0),
    EsiScope.ESI_CORPORATIONS_READ_DIVISIONS_V1: ESIScope(0),
    EsiScope.ESI_CORPORATIONS_READ_FACILITIES_V1: ESIScope(0),
    EsiScope.ESI_CORPORATIONS_READ_FW_STATS_V1: ESIScope(0),
    EsiScope.ESI_CORPORATIONS_READ_MEDALS_V1: ESIScope(0),
    EsiScope.ESI_CORPORATIONS_READ_STANDINGS_V1: ESIScope(0),
    EsiScope.ESI_CORPORATIONS_READ_STARBASES_V1: ESIScope(0),
    EsiScope.ESI_CORPORATIONS_READ_STRUCTURES_V1: ESIScope(0),
    EsiScope.ESI_CORPORATIONS_READ_TITLES_V1: ESIScope(0),
    EsiScope.ESI_CORPORATIONS_TRACK_MEMBERS_V1: ESIScope(0),
    EsiScope.ESI_FITTINGS_READ_FITTINGS_V1: ESIScope(0),
    EsiScope.ESI_FITTINGS_WRITE_FITTINGS_V1: ESIScope(1),
    EsiScope.ESI_FLEETS_READ_FLEET_V1: ESIScope(0),
    EsiScope.ESI_FLEETS_WRITE_FLEET_V1: ESIScope(1),
    EsiScope.ESI_INDUSTRY_READ_CHARACTER_JOBS_V1: ESIScope(0),
    EsiScope.ESI_INDUSTRY_READ_CHARACTER_MINING_V1: ESIScope(0),
    EsiScope.ESI_INDUSTRY_READ_CORPORATION_JOBS_V1: ESIScope(0),
    EsiScope.ESI_INDUSTRY_READ_CORPORATION_MINING_V1: ESIScope(0),
    EsiScope.ESI_KILLMAILS_READ_CORPORATION_KILLMAILS_V1: ESIScope(0),
    EsiScope.ESI_KILLMAILS_READ_KILLMAILS_V1: ESIScope(0),
    EsiScope.ESI_LOCATION_READ_LOCATION_V1: ESIScope(0),
    EsiScope.ESI_LOCATION_READ_ONLINE_V1: ESIScope(0),
    EsiScope.ESI_LOCATION_READ_SHIP_TYPE_V1: ESIScope(0),
    EsiScope.ESI_MAIL_ORGANIZE_MAIL_V1: ESIScope(1),
    EsiScope.ESI_MAIL_READ_MAIL_V1: ESIScope(0),
    EsiScope.ESI_MAIL_SEND_MAIL_V1: ESIScope(1),
    EsiScope.ESI_MARKETS_READ_CHARACTER_ORDERS_V1: ESIScope(0),
    EsiScope.ESI_MARKETS_READ_CORPORATION_ORDERS_V1: ESIScope(0),
    EsiScope.ESI_MARKETS_STRUCTURE_MARKETS_V1: ESIScope(1),
    EsiScope.ESI_PLANETS_MANAGE_PLANETS_V1: ESIScope(1),
    EsiScope.ESI_PLANETS_READ_CUSTOMS_OFFICES_V1: ESIScope(0),
    EsiScope.ESI_SEARCH_SEARCH_STRUCTURES_V1: ESIScope(0),
    EsiScope.ESI_SKILLS_READ_SKILLQUEUE_V1: ESIScope(0),
    EsiScope.ESI_SKILLS_READ_SKILLS_V1: ESIScope(0),
    EsiScope.ESI_UI_OPEN_WINDOW_V1: ESIScope(1),
    EsiScope.ESI_UI_WRITE_WAYPOINT_V1: ESIScope(1),
    EsiScope.ESI_UNIVERSE_READ_STRUCTURES_V1: ESIScope(0),
    EsiScope.ESI_WALLET_READ_CHARACTER_WALLET_V1: ESIScope(0),
    EsiScope.ESI_WALLET_READ_CORPORATION_WALLET_V1: ESIScope(0),
    EsiScope.ESI_WALLET_READ_CORPORATION_WALLETS_V1: ESIScope(0),
    EsiScope.PUBLICDATA: AbsoluteScope(0),
    "sni.create_coalition": AbsoluteScope(9),
    "sni.track_coalition": AbsoluteScope(9),
    "sni.create_dyn_token": AbsoluteScope(10),
    "sni.create_group": AbsoluteScope(9),
    "sni.create_per_token": AbsoluteScope(10),
    "sni.create_use_token": AbsoluteScope(0),
    "sni.create_user": AbsoluteScope(9),
    "sni.delete_coalition": AbsoluteScope(9),
    "sni.delete_crash_report": AbsoluteScope(10),
    "sni.delete_dyn_token": AbsoluteScope(10),
    "sni.delete_group": AbsoluteScope(9),
    "sni.delete_per_token": AbsoluteScope(10),
    "sni.delete_use_token": AbsoluteScope(10),
    "sni.delete_user": AbsoluteScope(9),
    "sni.discord.auth": AbsoluteScope(0),
    "sni.discord.read_user": AbsoluteScope(0),
    "sni.read_coalition": AbsoluteScope(0),
    "sni.read_crash_report": AbsoluteScope(10),
    "sni.read_dyn_token": AbsoluteScope(9),
    "sni.read_group": AbsoluteScope(0),
    "sni.read_own_token": AbsoluteScope(0),
    "sni.read_per_token": AbsoluteScope(9),
    "sni.read_use_token": AbsoluteScope(0),
    "sni.read_user": AbsoluteScope(0),
    "sni.set_authorized_to_login": AbsoluteScope(9),
    "sni.set_clearance_level_0": ClearanceModificationScope(0),
    "sni.set_clearance_level_1": ClearanceModificationScope(1),
    "sni.set_clearance_level_10": ClearanceModificationScope(10),
    "sni.set_clearance_level_2": ClearanceModificationScope(2),
    "sni.set_clearance_level_3": ClearanceModificationScope(3),
    "sni.set_clearance_level_4": ClearanceModificationScope(4),
    "sni.set_clearance_level_5": ClearanceModificationScope(5),
    "sni.set_clearance_level_6": ClearanceModificationScope(6),
    "sni.set_clearance_level_7": ClearanceModificationScope(7),
    "sni.set_clearance_level_8": ClearanceModificationScope(8),
    "sni.set_clearance_level_9": ClearanceModificationScope(9),
    "sni.teamspeak.auth": AbsoluteScope(0),
    "sni.teamspeak.read_user": AbsoluteScope(0),
    "sni.teamspeak.update_group_mapping": AbsoluteScope(9),
    "sni.update_coalition": AbsoluteScope(9),
    "sni.update_dyn_token": AbsoluteScope(10),
    "sni.update_group": AbsoluteScope(9),
    "sni.update_per_token": AbsoluteScope(10),
    "sni.update_use_token": AbsoluteScope(0),
    "sni.update_user": AbsoluteScope(9),
    "sni.system.read_configuration": AbsoluteScope(10),
    "sni.system.read_jobs": AbsoluteScope(10),
    "sni.system.submit_job": AbsoluteScope(10),
    "sni.fetch_corporation": AbsoluteScope(8),
    "sni.track_corporation": ESIScope(0),
    "sni.create_corporation_guest": ESIScope(0),
    "sni.delete_corporation_guest": ESIScope(1),
    "sni.read_corporation_guests": ESIScope(0),
    "sni.read_corporation": AbsoluteScope(0),
    "sni.update_corporation": ESIScope(1),
    "sni.fetch_alliance": AbsoluteScope(8),
    "sni.track_alliance": ESIScope(0),
    "sni.read_alliance": AbsoluteScope(0),
    "sni.update_alliance": ESIScope(1),
}


def are_in_same_alliance(user1: User, user2: User) -> bool:
    """
    Tells wether two users are in the same alliance. Users that have no
    alliance are considered in a different alliance as everyone else.
    """
    if (
        user1.corporation is None
        or user1.corporation.alliance is None
        or user2.corporation is None
        or user2.corporation.alliance is None
    ):
        return False
    return user1.corporation.alliance == user2.corporation.alliance


def are_in_same_coalition(user1: User, user2: User) -> bool:
    """
    Tells wether two users have a coalition in common.
    """
    if user1.corporation is None or user1.corporation.alliance is None:
        return False
    if user2.corporation is None or user2.corporation.alliance is None:
        return False
    for coa in Coalition.objects(members=user1.corporation.alliance):
        if user2.corporation.alliance in coa.members:
            return True
    return False


def are_in_same_corporation(user1: User, user2: User) -> bool:
    """
    Tells wether two users are in the same corporation. Users that have no
    corporation are considered in different a corporation as everyone else.
    """
    if user1.corporation is None or user2.corporation is None:
        return False
    return user1.corporation == user2.corporation


def assert_has_clearance(
    source: User, scope: str, target: Optional[User] = None
) -> None:
    """
    Like :meth:`sni.uac.clearance.has_clearance` but raises a
    :class:`PermissionError` if the result is ``False``.
    """
    if not has_clearance(source, scope, target):
        raise PermissionError


def distance_penalty(source: User, target: User) -> int:
    """
    Returns 0 if both users are the same user; returns 1 if they are not the
    same but in the same corporation; 3 if they are not in the same corporation
    but in the same alliance; 5 if they are not in the same alliance but in the
    same coalition; and otherwise, returns 7.
    """
    if source == target:
        return 0
    if are_in_same_corporation(source, target):
        return 1
    if are_in_same_alliance(source, target):
        return 3
    if are_in_same_coalition(source, target):
        return 5
    return 7


def has_clearance(
    source: User, scope_name: str, target: Optional[User] = None
) -> bool:
    """
    Check wether the *source* user has sufficient clearance to perform a given
    action (or *scope*) against the *target* user.
    """
    scope = SCOPES.get(scope_name)
    if scope is None:
        logging.warning('Unknown scope "%s"', scope_name)
        return False
    cache_key = [
        source.character_id,
        scope_name,
        target.character_id if target is not None else None,
    ]
    result = cache_get(cache_key)
    if not isinstance(result, bool):
        result = scope.has_clearance(source, target)
        cache_set(cache_key, result)
    logging.debug(
        "Access %s --[%s]--> %s %s",
        source.character_name,
        scope_name,
        target.character_name if target is not None else "N/A",
        "granted" if result else "denied",
    )
    return result


def reset_clearance(usr: User, save: bool = False):
    """
    Resets a user's clearance.

    If a user is the CEO of its corporation, then a clearance level of 2 is
    granted. If its corporation is the executor of the alliance, then a level
    of 4 is granted instead. If the user is root or has a clearance level of
    10, then a level of 10 is applied (so that superusers are preserved no
    matter what). Otherwise, the user's clearance level is set to 0.
    """
    if usr.clearance_level >= 9:
        return
    if usr.character_id == 0:
        usr.clearance_level = 10
    elif usr.is_ceo_of_alliance():
        usr.clearance_level = 4
    elif usr.is_ceo_of_corporation():
        usr.clearance_level = 2
    elif usr.clearance_level >= 0:
        usr.clearance_level = 0
    if save:
        logging.debug(
            "Reset clearance level of %s to %d",
            usr.character_name,
            usr.clearance_level,
        )
        usr.save()
