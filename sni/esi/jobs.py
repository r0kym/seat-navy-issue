"""
Some jobs to he scheduled, regarding the state of the database (e.g. making
sure all users are in the good corp, etc.)
"""

import logging

from sni.scheduler import scheduler
import sni.esi.esi as esi
import sni.uac.clearance as clearance
import sni.uac.user as user
import sni.time as time


def schedule_jobs():
    """
    Schedules all the jobs of this module.
    """
    scheduler.add_job(update_alliances, 'interval', minutes=60)
    scheduler.add_job(update_corporations, 'interval', minutes=60)
    scheduler.add_job(update_users, 'interval', minutes=60)


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
            logging.debug('Corporation of user %s changed',
                          usr.character_name)
            clearance.reset_clearance(usr)
        usr.save()
