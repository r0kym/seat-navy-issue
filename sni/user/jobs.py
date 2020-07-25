"""
User and eve player structure management jobs.
"""

import logging

import mongoengine as me

from sni.esi.esi import esi_get
from sni.esi.token import (
    EsiRefreshToken,
    get_access_token,
)
from sni.scheduler import scheduler
from sni.uac.clearance import reset_clearance
import sni.utils as utils

from .models import (
    Alliance,
    Coalition,
    Corporation,
    User,
)
from .user import (
    ensure_alliance,
    ensure_autogroup,
    ensure_corporation,
    ensure_user,
)


def update_alliance_autogroup(alliance: Alliance):
    """
    Updates an alliance autogroup.
    """
    logging.debug('Updating autogroup of alliance %s', alliance.alliance_name)
    grp = ensure_autogroup(alliance.alliance_name)
    try:
        grp.owner = alliance.executor.ceo
    except me.DoesNotExist:
        grp.owner = None
    grp.members = list(alliance.user_iterator())
    grp.save()


@scheduler.scheduled_job('interval',
                         hours=1,
                         start_date=utils.now_plus(minutes=10))
def update_alliance_autogroups():
    """
    Resets all the alliance autogroup. Instead of querying the ESI, it queries
    the database for all user in the corporations in that alliance, assuming
    the user and corporation records are up-to-date.
    """
    for alliance in Alliance.objects():
        scheduler.add_job(update_alliance_autogroup, args=(alliance, ))


def ensure_alliance_members(alliance: Alliance):
    """
    Makes sure all members of a given alliance exist in the database.
    """
    logging.debug('Updating members of alliance %s', alliance.alliance_name)
    response = esi_get(
        f'latest/alliances/{alliance.alliance_id}/corporations/')
    for corporation_id in response.data:
        ensure_corporation(corporation_id)


@scheduler.scheduled_job('interval', hours=1)
def ensure_alliances_members():
    """
    Iterates through all alliances (in the database) and makes sure their
    member corporations exist in the database. See
    :meth:`sni.user.jobs.ensure_alliance_members`.
    """
    for alliance in Alliance.objects:
        scheduler.add_job(ensure_alliance_members, args=(alliance, ))


def update_alliance_from_esi(alliance: Alliance):
    """
    Updates an alliance's properties from the ESI.
    """
    logging.debug('Updating properties of alliance %s', alliance.alliance_name)
    data = esi_get(f'latest/alliances/{alliance.alliance_id}').data
    alliance.executor_corporation_id = data['executor_corporation_id']
    alliance.save()


@scheduler.scheduled_job('interval', days=1)
def update_alliances_from_esi():
    """
    Updates the alliances properties from the ESI.
    """
    for alliance in Alliance.objects:
        scheduler.add_job(update_alliance_from_esi, args=(alliance, ))


def update_coalition_autogroup(coalition: Coalition):
    """
    Resets the coalition autogroup. Instead of querying the ESI, it queries
    the database for all user in that coalition, assuming the user, coalition,
    and alliance records are up-to-date.
    """
    logging.debug('Updating autogroup of coalition %s',
                  coalition.coalition_name)
    grp = ensure_autogroup(coalition.coalition_name)
    grp.members = list(coalition.user_iterator())
    grp.save()


@scheduler.scheduled_job('interval',
                         hours=1,
                         start_date=utils.now_plus(minutes=10))
def update_coalition_autogroups():
    """
    Resets the coalition autogroups.
    """
    for coalition in Coalition.objects():
        scheduler.add_job(update_coalition_autogroup, args=(coalition, ))


def update_corporation_autogroup(corporation: Corporation):
    """
    Resets the corporations autogroup. Instead of querying the ESI, it queries
    the database for all user in that corporation, assuming the user records
    are up-to-date.
    """
    logging.debug('Updating autogroup of corporation %s',
                  corporation.corporation_name)
    grp = ensure_autogroup(corporation.corporation_name)
    try:
        grp.owner = corporation.ceo
    except me.DoesNotExist:
        grp.owner = None
    grp.members = list(corporation.user_iterator())
    grp.save()


@scheduler.scheduled_job('interval',
                         hours=1,
                         start_date=utils.now_plus(minutes=10))
def update_corporation_autogroups():
    """
    Resets the corporations autogroups.
    """
    for corporation in Corporation.objects():
        scheduler.add_job(update_corporation_autogroup, args=(corporation, ))


def ensure_corporation_members(corporation: Corporation):
    """
    Ensure that all members of a corporation exist in the database.
    """
    logging.debug('Ensuring members of corporation %s',
                  corporation.corporation_name)
    scope = 'esi-corporations.read_corporation_membership.v1'
    # pylint: disable=protected-access
    query = EsiRefreshToken.objects.aggregate([
        {
            '$lookup': {
                'as': 'owner_data',
                'foreignField': '_id',
                'from': User._get_collection_name(),
                'localField': 'owner',
            },
        },
        {
            '$match': {
                'owner_data.corporation': corporation.pk,
                'scopes': scope,
                'valid': True,
            },
        },
        {
            '$project': {
                'owner_data.character_id': 1,
            },
        },
    ])
    esi_access_token = get_access_token(
        query.next()['owner_data'][0]['character_id'],
        scope,
    )
    response = esi_get(
        f'latest/corporations/{corporation.corporation_id}/members/',
        esi_access_token.access_token,
    )
    for character_id in response.data:
        scheduler.add_job(ensure_user, args=(character_id, ))


@scheduler.scheduled_job('interval', hours=1)
def ensure_corporations_members():
    """
    Iterates through all corporations (in the database) and makes sure their
    members exist in the database. See
    :meth:`sni.user.jobs.ensure_corporation_members`.
    """
    for corporation in Corporation.objects:
        scheduler.add_job(ensure_corporation_members, args=(corporation, ))


def update_corporation(corporation: Corporation):
    """
    Updates a corporation properties from the ESI.
    """
    logging.debug('Updating properties of corproation %s',
                  corporation.corporation_name)
    data = esi_get(f'latest/corporations/{corporation.corporation_id}').data
    corporation.alliance = ensure_alliance(
        data['alliance_id']) if 'alliance_id' in data else None
    corporation.ceo_character_id = int(data['ceo_id'])
    corporation.save()


@scheduler.scheduled_job('interval', days=1)
def update_corporations():
    """
    Updates corporations properties. (yes)
    """
    for corporation in Corporation.objects:
        scheduler.add_job(update_corporation, args=(corporation, ))


def update_user_autogroup(usr: User):
    """
    Makes sure a user belongs to its corporation, alliance, and coalitions
    autogroups.
    """
    if usr.corporation is not None:
        ensure_autogroup(
            usr.corporation.corporation_name).modify(add_to_set__members=usr)
    if usr.alliance is not None:
        ensure_autogroup(
            usr.alliance.alliance_name).modify(add_to_set__members=usr)
    for coalition in usr.coalitions():
        ensure_autogroup(
            coalition.coalition_name).modify(add_to_set__members=usr)


def update_user_from_esi(usr: User):
    """
    Updates a user's information from the ESI
    """
    data = esi_get(f'latest/characters/{usr.character_id}').data
    old_corporation = usr.corporation
    usr.corporation = ensure_corporation(data['corporation_id'])
    usr.updated_on = utils.now()
    if usr.corporation != old_corporation:
        logging.debug('Corporation of user %s changed', usr.character_name)
        reset_clearance(usr)
    usr.save()


@scheduler.scheduled_job('interval', hours=1)
def update_users_from_esi():
    """
    Iterated through all users and updates their field from ESI.
    """
    for usr in User.objects(character_id__gt=0):
        scheduler.add_job(update_user_from_esi, args=(usr, ))
