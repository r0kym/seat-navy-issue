"""
User and eve player structure management jobs.
"""

import logging

from sni.scheduler import scheduler
import sni.esi.esi as esi
import sni.esi.token as token
import sni.uac.clearance as clearance
import sni.user.group as group
import sni.user.user as user
import sni.utils as utils


def update_alliance_autogroup(alliance: user.Alliance):
    """
    Updates an alliance autogroup.
    """
    grp = group.ensure_autogroup(alliance.alliance_name)
    grp.owner = alliance.executor.ceo
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
    for alliance in user.Alliance.objects():
        logging.debug('Updating autogroup of alliance %s',
                      alliance.alliance_name)
        utils.catch_all(
            update_alliance_autogroup,
            f'Could not update autogroup of alliance {alliance.alliance_name}',
            args=[alliance])


def update_alliance_members(alliance: user.Alliance):
    """
    Makes sure all members of a given alliance exist in the database.
    """
    logging.debug('Updating members of alliance %s', alliance.alliance_name)
    response = esi.get(
        f'latest/alliances/{alliance.alliance_id}/corporations/')
    for corporation_id in response.json():
        user.ensure_corporation(corporation_id)


@scheduler.scheduled_job('interval', hours=1)
def update_alliances_members():
    """
    Iterates through all alliances (in the database) and makes sure their
    member corporations exist in the database. See
    :meth:`sni.user.jobs.update_alliance_members`.
    """
    for alliance in user.Alliance.objects:
        utils.catch_all(
            update_alliance_members,
            f'Failed to update members of alliance {alliance.alliance_name}',
            args=[alliance],
        )


def update_alliance(alliance: user.Alliance):
    """
    Updates an alliance's properties from the ESI.
    """
    logging.debug('Updating properties of alliance %s', alliance.alliance_name)
    data = esi.get(f'latest/alliances/{alliance.alliance_id}').json()
    alliance.executor_corporation_id = data['executor_corporation_id']
    alliance.save()


@scheduler.scheduled_job('interval', days=1)
def update_alliances():
    """
    Updates the alliances properties from the ESI.
    """
    for alliance in user.Alliance.objects:
        utils.catch_all(
            update_alliance,
            f'Failed to update properties of alliance {alliance.alliance_name}',
            args=[alliance],
        )


@scheduler.scheduled_job('interval',
                         hours=1,
                         start_date=utils.now_plus(minutes=10))
def update_coalition_autogroups():
    """
    Resets the coalition autogroups. Instead of querying the ESI, it queries
    the database for all user in that coalition, assuming the user, coalition,
    and alliance records are up-to-date.
    """
    for coalition in user.Coalition.objects():
        logging.debug('Updating autogroup of coalition %s', coalition.name)
        grp = group.ensure_autogroup(coalition.name)
        grp.members = list(coalition.user_iterator())
        grp.save()


@scheduler.scheduled_job('interval',
                         hours=1,
                         start_date=utils.now_plus(minutes=10))
def update_corporation_autogroups():
    """
    Resets the corporations autogroup. Instead of querying the ESI, it queries
    the database for all user in that corporation, assuming the user records
    are up-to-date.
    """
    for corporation in user.Corporation.objects():
        logging.debug('Updating autogroup of corporation %s',
                      corporation.corporation_name)
        grp = group.ensure_autogroup(corporation.corporation_name)
        grp.owner = corporation.ceo
        grp.members = list(corporation.user_iterator())
        grp.save()


def update_coropration_members(corporation: user.Corporation):
    """
    Ensure that all members of a corporation exist in the database.
    """
    logging.debug('Ensuring members of corporation %s',
                  corporation.corporation_name)
    scope = 'esi-corporations.read_corporation_membership.v1'
    # pylint: disable=protected-access
    query = token.EsiRefreshToken.objects.aggregate([
        {
            '$lookup': {
                'as': 'owner_data',
                'foreignField': '_id',
                'from': user.User._get_collection_name(),
                'localField': 'owner',
            },
        },
        {
            '$match': {
                'owner_data.corporation': corporation.pk,
                'scopes': scope,
            },
        },
        {
            '$project': {
                'owner_data.character_id': 1,
            },
        },
    ])
    esi_access_token = token.get_access_token(
        query.next()['owner_data'][0]['character_id'],
        scope,
    )
    response = esi.get(
        f'latest/corporations/{corporation.corporation_id}/members/',
        esi_access_token.access_token,
    )
    for character_id in response.json():
        user.ensure_user(character_id)


@scheduler.scheduled_job('interval', hours=1)
def update_corporations_members():
    """
    Iterates through all corporations (in the database) and makes sure their
    members exist in the database. See
    :meth:`sni.user.jobs.update_coropration_members`.
    """
    for corporation in user.Corporation.objects:
        utils.catch_all(
            update_coropration_members,
            'Failed to update members of corporation ' \
                + corporation.corporation_name,
            args=[corporation],
        )


def update_corporation(corporation: user.Corporation):
    """
    Updates a corporation properties from the ESI.
    """
    logging.debug('Updating properties of corproation %s',
                  corporation.corporation_name)
    data = esi.get(f'latest/corporations/{corporation.corporation_id}').json()
    corporation.alliance = user.ensure_alliance(
        data['alliance_id']) if 'alliance_id' in data else None
    corporation.ceo_character_id = int(data['ceo_id'])
    corporation.save()


@scheduler.scheduled_job('interval', days=1)
def update_corporations():
    """
    Updates corporations properties. (yes)
    """
    for corporation in user.Corporation.objects:
        utils.catch_all(
            update_corporation,
            'Failed to update properties of corporation ' \
                + corporation.corporation_name,
            args=[corporation],
        )


@scheduler.scheduled_job('interval', hours=1)
def update_users():
    """
    Iterated through all users and updates their field from ESI.
    """
    for usr in user.User.objects(character_id__gt=0):
        data = esi.get(f'latest/characters/{usr.character_id}').json()
        old_corporation = usr.corporation
        usr.corporation = user.ensure_corporation(data['corporation_id'])
        usr.updated_on = utils.now()
        if usr.corporation != old_corporation:
            logging.debug('Corporation of user %s changed', usr.character_name)
            clearance.reset_clearance(usr)
        usr.save()