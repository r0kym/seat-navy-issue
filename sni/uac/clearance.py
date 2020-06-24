"""
Clearance management and verification

Todo:
    Safer implementation. Right now it is too prone to coding errors when
    calling :meth:`sni.uac.clearance.assert_has_clearance`.
"""

import logging
from typing import Dict, Optional

import sni.uac.user as user

SCOPE_LEVELS: Dict[str, int] = {
    'esi-alliances.read_contacts.v1': 0,
    'esi-assets.read_assets.v1': 0,
    'esi-assets.read_corporation_assets.v1': 0,
    'esi-bookmarks.read_character_bookmarks.v1': 0,
    'esi-bookmarks.read_corporation_bookmarks.v1': 0,
    'esi-calendar.read_calendar_events.v1': 0,
    'esi-calendar.respond_calendar_events.v1': 1,
    'esi-characters.read_agents_research.v1': 0,
    'esi-characters.read_blueprints.v1': 0,
    'esi-characters.read_chat_channels.v1': 0,
    'esi-characters.read_contacts.v1': 0,
    'esi-characters.read_corporation_roles.v1': 0,
    'esi-characters.read_fatigue.v1': 0,
    'esi-characters.read_fw_stats.v1': 0,
    'esi-characters.read_loyalty.v1': 0,
    'esi-characters.read_medals.v1': 0,
    'esi-characters.read_notifications.v1': 0,
    'esi-characters.read_opportunities.v1': 0,
    'esi-characters.read_standings.v1': 0,
    'esi-characters.read_titles.v1': 0,
    'esi-characters.write_contacts.v1': 1,
    'esi-characterstats.read.v1': 0,
    'esi-clones.read_clones.v1': 0,
    'esi-clones.read_implants.v1': 0,
    'esi-contracts.read_character_contracts.v1': 0,
    'esi-contracts.read_corporation_contracts.v1': 0,
    'esi-corporations.read_blueprints.v1': 0,
    'esi-corporations.read_contacts.v1': 0,
    'esi-corporations.read_container_logs.v1': 0,
    'esi-corporations.read_corporation_membership.v1': 0,
    'esi-corporations.read_divisions.v1': 0,
    'esi-corporations.read_facilities.v1': 0,
    'esi-corporations.read_fw_stats.v1': 0,
    'esi-corporations.read_medals.v1': 0,
    'esi-corporations.read_standings.v1': 0,
    'esi-corporations.read_starbases.v1': 0,
    'esi-corporations.read_structures.v1': 0,
    'esi-corporations.read_titles.v1': 0,
    'esi-corporations.track_members.v1': 0,
    'esi-fittings.read_fittings.v1': 0,
    'esi-fittings.write_fittings.v1': 1,
    'esi-fleets.read_fleet.v1': 0,
    'esi-fleets.write_fleet.v1': 1,
    'esi-industry.read_character_jobs.v1': 0,
    'esi-industry.read_character_mining.v1': 0,
    'esi-industry.read_corporation_jobs.v1': 0,
    'esi-industry.read_corporation_mining.v1': 0,
    'esi-killmails.read_corporation_killmails.v1': 0,
    'esi-killmails.read_killmails.v1': 0,
    'esi-location.read_location.v1': 0,
    'esi-location.read_online.v1': 0,
    'esi-location.read_ship_type.v1': 0,
    'esi-mail.organize_mail.v1': 1,
    'esi-mail.read_mail.v1': 0,
    'esi-mail.send_mail.v1': 1,
    'esi-markets.read_character_orders.v1': 0,
    'esi-markets.read_corporation_orders.v1': 0,
    'esi-markets.structure_markets.v1': 1,
    'esi-planets.manage_planets.v1': 1,
    'esi-planets.read_customs_offices.v1': 0,
    'esi-search.search_structures.v1': 0,
    'esi-skills.read_skillqueue.v1': 0,
    'esi-skills.read_skills.v1': 0,
    'esi-ui.open_window.v1': 1,
    'esi-ui.write_waypoint.v1': 1,
    'esi-universe.read_structures.v1': 0,
    'esi-wallet.read_character_wallet.v1': 0,
    'esi-wallet.read_corporation_wallet.v1': 0,
    'esi-wallet.read_corporation_wallets.v1': 0,
    'publicData': 0,
    'sni.delete_user': 9,
    'sni.read_coalition': 0,
    'sni.read_group': 0,
    'sni.write_coalition': 9,
    'sni.write_group': 9,
    'sni.read_own_token': 0,
    'sni.write_dyn_token': 10,
    'sni.write_per_token': 10,
    'sni.write_use_token': 0,
    'sni.set_clearance_level_0': 0,
    'sni.set_clearance_level_1': 1,
    'sni.set_clearance_level_2': 2,
    'sni.set_clearance_level_3': 3,
    'sni.set_clearance_level_4': 4,
    'sni.set_clearance_level_5': 5,
    'sni.set_clearance_level_6': 6,
    'sni.set_clearance_level_7': 7,
    'sni.set_clearance_level_8': 8,
    'sni.set_clearance_level_9': 9,
    'sni.set_clearance_level_10': 10,
}


def are_in_same_alliance(user1: user.User, user2: user.User) -> bool:
    """
    Tells wether two users are in the same alliance. Users that have no
    alliance are considered in a different alliance as everyone else.
    """
    if user1.corporation.alliance is None or user2.corporation.alliance is None:
        return False
    return user1.corporation.alliance == user2.corporation.alliance


def are_in_same_coalition(user1: user.User, user2: user.User) -> bool:
    """
    Tells wether two users have a coalition in common.
    """
    if user1.corporation is None or user1.corporation.alliance is None:
        return False
    if user2.corporation is None or user2.corporation.alliance is None:
        return False
    for coa in user.Coalition.objects(members=user1.corporation.alliance):
        if user2.corporation.alliance in coa.members:
            return True
    return False


def are_in_same_corporation(user1: user.User, user2: user.User) -> bool:
    """
    Tells wether two users are in the same corporation. Users that have no
    corporation are considered in different a corporation as everyone else.
    """
    if user1.corporation is None or user2.corporation is None:
        return False
    return user1.corporation == user2.corporation


def assert_has_clearance(source: user.User,
                         scope: str,
                         target: Optional[user.User] = None) -> None:
    """
    Like :meth:`sni.uac.clearance.has_clearance` but raises a
    :class:`PermissionError` if the result is ``False``.
    """
    if not has_clearance(source, scope, target):
        raise PermissionError


def distance_penalty(source: user.User, target: Optional[user.User]) -> int:
    """
    Returns 0 if both users are the same user, of if the source has clearance
    level >= 7, or if the target is ``None``; returns 1 if they are not the
    same but in the same corporation; 3 if they are not in the same corporation
    but in the same alliance; 5 if they are not in the same alliance but in the
    same coalition; and otherwise, returns 10.
    """
    if source.clearance_level >= 7 or target is None or source == target:
        return 0
    if are_in_same_corporation(source, target):
        return 1
    if are_in_same_alliance(source, target):
        return 3
    if are_in_same_coalition(source, target):
        return 5
    return 10


def has_clearance(source: user.User,
                  scope: str,
                  target: Optional[user.User] = None) -> bool:
    """
    Check wether the *source* user has sufficient clearance to perform a given
    action (or *scope*) against the *target* user. For actions regarding the
    SNI instance (like administrative and maintenance tasks), the target should
    be ``None``.

    If the scope is not about changing clearance levels (so of the form
    ``sni.set_clearance_level_X`), then the required clearance is calculated
    with the formula::

        required_clearance = min(distance_penalty + scope_level, 10)

    where

    * the **distance penalty**, prepresent "how far" the source is the target
      (see :meth:`sni.uac.clearance.distance_penalty`);

    * the **scope level**, is a factor that depends on the scope.

    If the scope *is* about changing clearance levels (so of the form
    ``sni.set_clearance_level_X` where 0 <= X <= 10), and if t is the clearance
    level of the target, then::

        required_clearance =
            X   if t <= X,
            9   if t > X

    Note that in the case, X is also the scope level of the scope.
    """
    if scope not in SCOPE_LEVELS:
        logging.warning('Unknown scope %s', scope)
        raise PermissionError
    scope_level = SCOPE_LEVELS[scope]
    if scope.startswith('sni.set_clearance_level_'):  # Clearance scopes
        if target is None:
            raise ValueError('Clearance scopes must have a valid target')
        if target.clearance_level <= scope_level:
            required_clearance = scope_level
        else:
            required_clearance = 9
    else:  # Other scopes
        required_clearance = min(
            distance_penalty(source, target) + scope_level, 10)
    logging.debug(
        'Access %s --[%s]--> %s requires a clearance of %d, source has %d',
        source.character_name,
        scope,
        target.character_name if target is not None else 'None',
        required_clearance,
        source.clearance_level,
    )
    return source.clearance_level >= required_clearance
