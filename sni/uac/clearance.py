"""
Clearance management and verification. Each user has a **clearance level**,
which is an integer:

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
    "esi-alliances.read_contacts.v1": ESIScope(0),
    "esi-assets.read_assets.v1": ESIScope(0),
    "esi-assets.read_corporation_assets.v1": ESIScope(0),
    "esi-bookmarks.read_character_bookmarks.v1": ESIScope(0),
    "esi-bookmarks.read_corporation_bookmarks.v1": ESIScope(0),
    "esi-calendar.read_calendar_events.v1": ESIScope(0),
    "esi-calendar.respond_calendar_events.v1": ESIScope(1),
    "esi-characters.read_agents_research.v1": ESIScope(0),
    "esi-characters.read_blueprints.v1": ESIScope(0),
    "esi-characters.read_chat_channels.v1": ESIScope(0),
    "esi-characters.read_contacts.v1": ESIScope(0),
    "esi-characters.read_corporation_roles.v1": ESIScope(0),
    "esi-characters.read_fatigue.v1": ESIScope(0),
    "esi-characters.read_fw_stats.v1": ESIScope(0),
    "esi-characters.read_loyalty.v1": ESIScope(0),
    "esi-characters.read_medals.v1": ESIScope(0),
    "esi-characters.read_notifications.v1": ESIScope(0),
    "esi-characters.read_opportunities.v1": ESIScope(0),
    "esi-characters.read_standings.v1": ESIScope(0),
    "esi-characters.read_titles.v1": ESIScope(0),
    "esi-characters.write_contacts.v1": ESIScope(1),
    "esi-characterstats.read.v1": ESIScope(0),
    "esi-clones.read_clones.v1": ESIScope(0),
    "esi-clones.read_implants.v1": ESIScope(0),
    "esi-contracts.read_character_contracts.v1": ESIScope(0),
    "esi-contracts.read_corporation_contracts.v1": ESIScope(0),
    "esi-corporations.read_blueprints.v1": ESIScope(0),
    "esi-corporations.read_contacts.v1": ESIScope(0),
    "esi-corporations.read_container_logs.v1": ESIScope(0),
    "esi-corporations.read_corporation_membership.v1": ESIScope(0),
    "esi-corporations.read_divisions.v1": ESIScope(0),
    "esi-corporations.read_facilities.v1": ESIScope(0),
    "esi-corporations.read_fw_stats.v1": ESIScope(0),
    "esi-corporations.read_medals.v1": ESIScope(0),
    "esi-corporations.read_standings.v1": ESIScope(0),
    "esi-corporations.read_starbases.v1": ESIScope(0),
    "esi-corporations.read_structures.v1": ESIScope(0),
    "esi-corporations.read_titles.v1": ESIScope(0),
    "esi-corporations.track_members.v1": ESIScope(0),
    "esi-fittings.read_fittings.v1": ESIScope(0),
    "esi-fittings.write_fittings.v1": ESIScope(1),
    "esi-fleets.read_fleet.v1": ESIScope(0),
    "esi-fleets.write_fleet.v1": ESIScope(1),
    "esi-industry.read_character_jobs.v1": ESIScope(0),
    "esi-industry.read_character_mining.v1": ESIScope(0),
    "esi-industry.read_corporation_jobs.v1": ESIScope(0),
    "esi-industry.read_corporation_mining.v1": ESIScope(0),
    "esi-killmails.read_corporation_killmails.v1": ESIScope(0),
    "esi-killmails.read_killmails.v1": ESIScope(0),
    "esi-location.read_location.v1": ESIScope(0),
    "esi-location.read_online.v1": ESIScope(0),
    "esi-location.read_ship_type.v1": ESIScope(0),
    "esi-mail.organize_mail.v1": ESIScope(1),
    "esi-mail.read_mail.v1": ESIScope(0),
    "esi-mail.send_mail.v1": ESIScope(1),
    "esi-markets.read_character_orders.v1": ESIScope(0),
    "esi-markets.read_corporation_orders.v1": ESIScope(0),
    "esi-markets.structure_markets.v1": ESIScope(1),
    "esi-planets.manage_planets.v1": ESIScope(1),
    "esi-planets.read_customs_offices.v1": ESIScope(0),
    "esi-search.search_structures.v1": ESIScope(0),
    "esi-skills.read_skillqueue.v1": ESIScope(0),
    "esi-skills.read_skills.v1": ESIScope(0),
    "esi-ui.open_window.v1": ESIScope(1),
    "esi-ui.write_waypoint.v1": ESIScope(1),
    "esi-universe.read_structures.v1": ESIScope(0),
    "esi-wallet.read_character_wallet.v1": ESIScope(0),
    "esi-wallet.read_corporation_wallet.v1": ESIScope(0),
    "esi-wallet.read_corporation_wallets.v1": ESIScope(0),
    "publicData": AbsoluteScope(0),
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
    "sni.read_corporation": AbsoluteScope(0),
    "sni.fetch_alliance": AbsoluteScope(8),
    "sni.track_alliance": ESIScope(0),
    "sni.read_alliance": AbsoluteScope(0),
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
    if usr.character_id == 0 or usr.clearance_level == 10:
        usr.clearance_level = 10
    elif usr.is_ceo_of_alliance():
        usr.clearance_level = 4
    elif usr.is_ceo_of_corporation():
        usr.clearance_level = 2
    else:
        usr.clearance_level = 0
    logging.debug(
        "Reset clearance level of %s to %d",
        usr.character_name,
        usr.clearance_level,
    )
    if save:
        usr.save()
