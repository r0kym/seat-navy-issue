"""
User and eve player structure management jobs.
"""

import logging

from sni.scheduler import scheduler

import sni.esi.token as token
import sni.esi.esi as esi
import sni.user.user as user


def update_alliance_properties(alliance: user.Alliance):
    """
    Updates an alliance's properties from the ESI.
    """
    logging.debug('Updating properties of alliance %s', alliance.alliance_name)
    data = esi.get(f'latest/alliances/{alliance.alliance_id}').json()
    alliance.executor_corporation_id = data['executor_corporation_id']
    alliance.save()


@scheduler.scheduled_job('interval', days=1)
def update_alliances_properties():
    """
    Updates the alliances properties from the ESI.
    """
    for alliance in user.Alliance.objects:
        try:
            update_alliance_properties(alliance)
        except Exception as error:
            logging.error('Failed to update properties of alliance %s: %s',
                          alliance.alliance_name, str(error))


@scheduler.scheduled_job('interval', hours=1)
def update_alliances_members():
    """
    Iterates through all alliances (in the database) and makes sure their
    member corporations exist in the database. See
    :meth:`sni.user.jobs.update_alliance_members`.
    """
    for alliance in user.Alliance.objects:
        try:
            logging.debug('Updating members of alliance %s',
                          alliance.alliance_name)
            response = esi.get(
                f'latest/alliances/{alliance.alliance_id}/corporations/')
            for corporation_id in response.json():
                user.ensure_corporation(corporation_id)
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


@scheduler.scheduled_job('interval', hours=1)
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


def update_corporation_properties(corporation: user.Corporation):
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
def update_corporations_properties():
    """
    Updates corporations properties. (yes)
    """
    for corporation in user.Corporation.objects:
        try:
            update_corporation_properties(corporation)
        except Exception as error:
            logging.error('Failed to update properties of corporation %s: %s',
                          corporation.corporation_name, str(error))
