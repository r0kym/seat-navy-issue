"""
Recurrent teamspeak jobs
"""

import logging

from ts3.query import TS3Connection

from sni.scheduler import scheduler
import sni.conf as conf
import sni.teamspeak.teamspeak as ts


@scheduler.scheduled_job('interval', minutes=10)
def apply_teamspeak_group_mappings():
    """
    Iterates through the Teamspeak group mappings and applies them, see
    :meth:`sni.teamspeak.jobs.apply_teamspeak_group_mapping`.
    """
    connection = ts.new_connection()
    for ts_group in ts.group_list(connection):
        sgid = ts_group.sgid
        if ts.TeamspeakGroupMapping.objects(
                teamspeak_group_id=sgid).count() == 0:
            # Group is not registered in a mapping
            continue
        allowed_cldbids = ts.client_ids_mapped_to_group(sgid)
        current_cldbids = [
            raw['cldbid']
            for raw in connection.servergroupclientlist(sgid=sgid).parsed
        ]
        # Remove clients that should not be in group
        for cldbid in current_cldbids:
            if cldbid not in allowed_cldbids:
                connection.servergroupdelclient(cldbid=cldbid, sgid=sgid)
        # Add clients that should be in group
        for cldbid in allowed_cldbids:
            connection.servergroupaddclient(cldbid=cldbid, sgid=sgid)


def update_teamspeak_client(connection: TS3Connection,
                            client: ts.TeamspeakClient):
    """
    Update's a teamspeak client data and permissions, if that client is
    registered as a teamspeak user.
    """
    tsusr: ts.TeamspeakUser = ts.TeamspeakUser.objects(
        teamspeak_id=client.client_database_id).first()
    auth_group = ts.ensure_group(connection,
                                 conf.get('teamspeak.auth_group_name'))
    if tsusr is not None:
        logging.debug(
            'Updating known teamspeak client %s (%d) bound to user %s',
            client.client_nickname, client.client_database_id,
            tsusr.user.character_name)
        connection.clientedit(clid=client.clid,
                              client_description=tsusr.user.tickered_name)
        connection.servergroupaddclient(
            cldbid=client.client_database_id,
            sgid=auth_group.sgid,
        )
    else:
        logging.debug('Updating unknown teamspeak client %s (%d)',
                      client.client_nickname, client.client_database_id)
        connection.servergroupdelclient(
            cldbid=client.client_database_id,
            sgid=auth_group.sgid,
        )


@scheduler.scheduled_job('interval', minutes=10)
def update_teamspeak_clients():
    """
    Updates all teamspeak clients. See
    :meth:`sni.teamspeak.update_teamspeak_client`.
    """
    logging.info('Updating all teamspeak clients')
    connection = ts.new_connection()
    for client in ts.client_list(connection):
        try:
            update_teamspeak_client(connection, client)
        except Exception as error:
            logging.error('Failed to update client %s (%d): %s',
                          client.client_nickname, client.client_database_id,
                          str(error))
