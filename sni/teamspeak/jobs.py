"""
Recurrent teamspeak jobs
"""

import logging
from typing import List

import ts3.query

from sni.scheduler import scheduler
import sni.conf as conf
import sni.utils as utils
import sni.teamspeak.teamspeak as ts
import sni.user.group as group
import sni.user.user as user


@scheduler.scheduled_job('interval', minutes=30)
def message_registered_clients_with_wrong_name():
    """
    Iterates through all users that are registered in Teamspeak, and checks
    their nickname. If it doesn't match, sends a message.
    """
    connection = ts.new_connection()
    for ts_client in ts.client_list(connection):
        if ts_client.client_nickname == conf.get('teamspeak.bot_name'):
            continue
        usr: user.User = user.User.objects(
            teamspeak_cldbid=ts_client.client_database_id).first()
        if usr is None:
            # TS client is unknown
            continue
        tickered_name = usr.tickered_name
        if ts_client.client_nickname != tickered_name:
            logging.debug('Wrong nickname found %s; should be %s',
                          ts_client.client_nickname, tickered_name)
            message = f'Hello {ts_client.client_nickname}. ' \
                + 'Please change your Teamspeak nickname to ' \
                + f'"{tickered_name}" (without the quotes). Thank you :)' \
                + ' -- SeAT Navy Issue Teamspeak Bot; This is an automated' \
                + ' message, please do not respond.'
            utils.catch_all(
                connection.sendtextmessage,
                f'Failed to notify teamspeak user {ts_client.client_nickname}',
                kwargs={
                    'targetmode': 1,
                    'target': ts_client.clid,
                    'msg': message,
                })


@scheduler.scheduled_job('interval', minutes=10)
def map_teamspeak_groups():
    """
    Creates all groups on Teamspeak.
    """
    connection = ts.new_connection()
    for grp in group.Group.objects(map_to_teamspeak=True):
        logging.debug('Mapping group %s to Teamspeak', grp.name)
        tsgrp = ts.ensure_group(connection, grp.name)
        grp.teamspeak_sgid = tsgrp.sgid
        grp.save()


@scheduler.scheduled_job('interval', minutes=10)
def update_teamspeak_groups():
    """
    Updates group memberships on Teamspeak
    """
    connection = ts.new_connection()
    for grp in group.Group.objects(map_to_teamspeak=True,
                                   teamspeak_sgid__exists=True):
        logging.debug('Updating Teamspeak group %s', grp.name)
        current_cldbids: List[int] = [
            int(raw['cldbid']) for raw in connection.servergroupclientlist(
                sgid=grp.teamspeak_sgid).parsed
        ]
        allowed_cldbids: List[int] = [
            usr.teamspeak_cldbid for usr in grp.members
            if 'teamspeak_cldbid' in usr
        ]
        for cldbid in current_cldbids:
            if cldbid in allowed_cldbids:
                continue
            try:
                connection.servergroupdelclient(
                    cldbid=cldbid,
                    sgid=grp.teamspeak_sgid,
                )
            except ts3.query.TS3QueryError as error:
                logging.error(
                    'Could not remove client %d from Teamspeak group %s: %s',
                    cldbid, grp.name, str(error))
        for cldbid in allowed_cldbids:
            if cldbid in current_cldbids:
                continue
            try:
                connection.servergroupaddclient(
                    sgid=grp.teamspeak_sgid,
                    cldbid=cldbid,
                )
            except ts3.query.TS3QueryError as error:
                logging.error(
                    'Could not add client %d to Teamspeak group %s: %s',
                    cldbid, grp.name, str(error))
