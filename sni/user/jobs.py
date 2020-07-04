"""
User and eve player structure management jobs.
"""

import logging

from sni.scheduler import scheduler

import sni.esi.token as token
import sni.esi.esi as esi
import sni.user.user as user


def update_alliance_members(alliance: user.Alliance):
    """
    Ensures that all member coproration of a given alliance exist in the
    database.
    """
    logging.debug('Updating members of alliance %s', alliance.alliance_name)
    response = esi.get(
        f'latest/alliances/{alliance.alliance_id}/corporations/')
    for corporation_id in response.json():
        user.ensure_corporation(corporation_id)


@scheduler.scheduled_job('interval', minutes=60)
def update_alliances_members():
    """
    Iterates through all alliances (in the database) and makes sure their
    member corporations exist in the database. See
    :meth:`sni.user.jobs.update_alliance_members`.
    """
    for alliance in user.Alliance.objects:
        try:
            update_alliance_members(alliance)
        except Exception as error:
            logging.error('Could not update members of alliance %s: %s',
                          alliance.alliance_name, str(error))


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


@scheduler.scheduled_job('interval', minutes=60)
def update_corporations_members():
    """
    Iterates through all corporations (in the database) and makes sure their
    members exist in the database. See
    :meth:`sni.user.jobs.update_coropration_members`.
    """
    for corporation in user.Corporation.objects:
        try:
            update_coropration_members(corporation)
        except Exception as error:
            logging.error('Could not update members of coproration %s: %s',
                          corporation.corporation_name, str(error))
