"""
Some jobs to he scheduled, regarding the state of the database (e.g. making
sure all users are in the good corp, etc.)
"""

import logging

from sni.scheduler import scheduler
import sni.esi.esi as esi
import sni.esi.sso as sso
import sni.esi.token as esitoken
import sni.time as time
import sni.uac.clearance as clearance
import sni.uac.user as user


@scheduler.scheduled_job('interval', minutes=60)
def refresh_tokens():
    """
    Iterates through the ESI refresh tokens and refreshes the corresponding ESI
    access tokens.
    """
    for refresh_token in esitoken.EsiRefreshToken.objects():
        usr = refresh_token.owner
        try:
            esitoken.save_esi_tokens(
                sso.refresh_access_token(refresh_token.refresh_token))
            logging.info('Refreshed token of %s', usr.character_name)
        except Exception as error:  # pylint: disable=broad-except
            logging.error('Could not refresh access token of %s: %s',
                          usr.character_name, str(error))


@scheduler.scheduled_job('interval', minutes=60)
def update_alliances():
    """
    Iterated through all alliances and updates their fields from ESI.
    """
    for alliance in user.Alliance.objects():
        data = esi.get(f'latest/alliances/{alliance.alliance_id}').json()
        alliance.executor_corporation_id = int(data['executor_corporation_id'])
        alliance.ticker = data['ticker']
        alliance.updated_on = time.now()
        alliance.save()


@scheduler.scheduled_job('interval',
                         minutes=60,
                         start_date=time.now_plus(minutes=10))
def update_alliance_autogroups():
    """
    Resets all the alliance autogroup. Instead of querying the ESI, it queries
    the database for all user in the corporations in that alliance, assuming
    the user and corporation records are up-to-date.
    """
    for alliance in user.Alliance.objects():
        logging.debug('Updating autogroup of alliance %s',
                      alliance.alliance_name)
        try:
            grp = user.ensure_auto_group(alliance.alliance_name)
            grp.owner = alliance.executor.ceo
            grp.members = list(alliance.user_iterator())
            grp.save()
        except Exception as error:  # pylint: disable=broad-except
            logging.error('Could not update autogroup of alliance %s: %s',
                          alliance.alliance_name, str(error))


@scheduler.scheduled_job('interval', minutes=60)
def update_corporations():
    """
    Iterated through all corporations and updates their fields from ESI.
    """
    for corporation in user.Corporation.objects():
        data = esi.get(
            f'latest/corporations/{corporation.corporation_id}').json()
        old_alliance = corporation.alliance
        if 'alliance_id' in data['alliance_id']:
            corporation.alliance = user.ensure_alliance(data['alliance_id'])
        corporation.ceo_character_id = int(data['ceo_id'])
        corporation.ticker = data['ticker']
        corporation.updated_on = time.now()
        if corporation.alliance != old_alliance:
            logging.debug('Alliance of corporation %s changed',
                          corporation.corporation_name)
            for usr in user.User.objects(corporation=corporation):
                clearance.reset_clearance(usr, save=True)
        corporation.save()


@scheduler.scheduled_job('interval',
                         minutes=60,
                         start_date=time.now_plus(minutes=10))
def update_coalition_autogroups():
    """
    Resets the coalition autogroups. Instead of querying the ESI, it queries
    the database for all user in that coalition, assuming the user, coalition,
    and alliance records are up-to-date.
    """
    for coalition in user.Coalition.objects():
        logging.debug('Updating autogroup of coalition %s', coalition.name)
        grp = user.ensure_auto_group(coalition.name)
        grp.members = list(coalition.user_iterator())
        grp.save()


@scheduler.scheduled_job('interval',
                         minutes=60,
                         start_date=time.now_plus(minutes=10))
def update_corporation_autogroups():
    """
    Resets the corporations autogroup. Instead of querying the ESI, it queries
    the database for all user in that corporation, assuming the user records
    are up-to-date.
    """
    for corporation in user.Corporation.objects():
        logging.debug('Updating autogroup of corporation %s',
                      corporation.corporation_name)
        grp = user.ensure_auto_group(corporation.corporation_name)
        grp.owner = corporation.ceo
        grp.members = list(corporation.user_iterator())
        grp.save()


@scheduler.scheduled_job('interval', minutes=60)
def update_users():
    """
    Iterated through all users and updates their field from ESI.
    """
    for usr in user.User.objects(character_id__gt=0):
        data = esi.get(f'latest/characters/{usr.character_id}').json()
        old_corporation = usr.corporation
        usr.corporation = user.ensure_corporation(data['corporation_id'])
        usr.updated_on = time.now()
        if usr.corporation != old_corporation:
            logging.debug('Corporation of user %s changed', usr.character_name)
            clearance.reset_clearance(usr)
        usr.save()
