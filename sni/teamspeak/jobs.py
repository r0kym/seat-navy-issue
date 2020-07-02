"""
Recurrent teamspeak jobs
"""

import logging
from typing import List

import ts3.query

from sni.scheduler import scheduler
import sni.teamspeak.teamspeak as ts
import sni.uac.group as group


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
            if cldbid not in allowed_cldbids:
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
            try:
                connection.servergroupaddclient(
                    sgid=grp.teamspeak_sgid,
                    cldbid=cldbid,
                )
            except ts3.query.TS3QueryError as error:
                logging.error(
                    'Could not add client %d to Teamspeak group %s: %s',
                    cldbid, grp.name, str(error))
