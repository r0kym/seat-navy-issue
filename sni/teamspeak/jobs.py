"""
Recurrent teamspeak jobs
"""

import logging
from typing import List

from ts3.query import TS3Connection, TS3QueryError

from sni.scheduler import scheduler
from sni.user.models import Group, User
from sni.conf import CONFIGURATION as conf
import sni.utils as utils

from .teamspeak import (
    cached_teamspeak_query,
    client_list,
    ensure_group,
    new_teamspeak_connection,
)


@scheduler.scheduled_job("interval", minutes=30)
def message_registered_clients_with_wrong_name():
    """
    Iterates through all users that are registered in Teamspeak, and checks
    their nickname. If it doesn't match, sends a message.
    """
    connection = new_teamspeak_connection()
    for ts_client in client_list(connection):
        if ts_client.client_nickname.startswith(conf.teamspeak.bot_name):
            # TS client is probably the bot
            continue
        usr: User = User.objects(
            teamspeak_cldbid=ts_client.client_database_id
        ).first()
        if usr is None:
            # TS client is unknown
            continue
        tickered_name = usr.tickered_name
        if ts_client.client_nickname != tickered_name:
            logging.debug(
                "Wrong nickname found %s; should be %s",
                ts_client.client_nickname,
                tickered_name,
            )
            message = (
                f"Hello {ts_client.client_nickname}. "
                + "Please change your Teamspeak nickname to "
                + f'"{tickered_name}" (without the quotes). Thank you :)'
                + " -- SeAT Navy Issue Teamspeak Bot; This is an automated"
                + " message, please do not respond."
            )
            utils.catch_all(
                connection.sendtextmessage,
                f"Failed to notify teamspeak user {ts_client.client_nickname}",
                kwargs={
                    "targetmode": 1,
                    "target": ts_client.clid,
                    "msg": message,
                },
            )
    connection.close()


@scheduler.scheduled_job("interval", minutes=10)
def map_teamspeak_groups():
    """
    Creates all groups on Teamspeak.
    """
    connection = new_teamspeak_connection()
    for grp in Group.objects(map_to_teamspeak=True):
        logging.debug("Mapping group %s to Teamspeak", grp.group_name)
        tsgrp = ensure_group(connection, grp.group_name)
        grp.teamspeak_sgid = tsgrp.sgid
        grp.save()
    connection.close()


@scheduler.scheduled_job("interval", minutes=10)
def update_teamspeak_groups():
    """
    Updates group memberships on Teamspeak
    """
    connection = new_teamspeak_connection()
    for grp in Group.objects(map_to_teamspeak=True, teamspeak_sgid__ne=None):
        logging.debug("Updating Teamspeak group %s", grp.group_name)
        current_cldbids: List[int] = [
            int(raw["cldbid"])
            for raw in cached_teamspeak_query(
                connection,
                TS3Connection.servergroupclientlist,
                300,
                kwargs={"sgid": grp.teamspeak_sgid},
            )
        ]
        allowed_cldbids: List[int] = [
            usr.teamspeak_cldbid
            for usr in grp.members
            if usr.teamspeak_cldbid is not None
        ]
        for cldbid in current_cldbids:
            if cldbid in allowed_cldbids:
                continue
            try:
                connection.servergroupdelclient(
                    cldbid=cldbid, sgid=grp.teamspeak_sgid,
                )
            except TS3QueryError as error:
                logging.error(
                    "Could not remove client %d from Teamspeak group %s: %s",
                    cldbid,
                    grp.group_name,
                    str(error),
                )
        for cldbid in allowed_cldbids:
            if cldbid in current_cldbids:
                continue
            try:
                connection.servergroupaddclient(
                    sgid=grp.teamspeak_sgid, cldbid=cldbid,
                )
            except TS3QueryError as error:
                logging.error(
                    "Could not add client %d to Teamspeak group %s: %s",
                    cldbid,
                    grp.group_name,
                    str(error),
                )
    connection.close()
