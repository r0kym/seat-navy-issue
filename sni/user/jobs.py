"""
User and eve player structure management jobs.
"""

import logging

from sni.scheduler import scheduler

import sni.esi.token as token
import sni.esi.esi as esi
import sni.user.user as user


def update_coropration_members(corporation: user.Corporation):
    """
    Ensure that all members of a corporation exist in the database.
    """
    logging.debug('Ensuring members of corporation %s',
                  corporation.corporation_name)
    # pylint: disable=protected-access
    query = token.EsiAccessToken.objects.aggregate([{
        '$lookup': {
            'as': 'owner_data',
            'foreignField': '_id',
            'from': user.User._get_collection_name(),
            'localField': 'owner',
        },
    }, {
        '$match': {
            'owner_data.corporation': corporation.pk,
            'scopes': 'esi-corporations.read_corporation_membership.v1',
        },
    }, {
        '$project': {
            'access_token': 1,
        },
    }])
    esi_token = query.next()['access_token']
    response = esi.get(
        f'latest/corporations/{corporation.corporation_id}/members/',
        esi_token,
    )
    for character_id in response.json():
        user.ensure_user(character_id)


@scheduler.scheduled_job('interval', minutes=60)
def update_corporations_members():
    """
    Iterates through all corporations (in the database) makes sure their
    members exist in the database.
    """
    for corporation in user.Corporation.objects:
        try:
            update_coropration_members(corporation)
        except Exception as error:
            logging.error('Could not update members of coproration %s: %s',
                          corporation.corporation_name, str(error))
