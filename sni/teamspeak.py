"""
Teamspeak management.

See also:
    `Teamspeak 3 query server documentation <https://drive.google.com/file/d/1d2y5daxBR7mo92g1IxOKB6A14Ok2-R7T/view?usp=sharing>`_
"""

import logging
import random
import string
from typing import List, Optional

import mongoengine as me
import pydantic
import ts3
import ts3.query

import sni.conf as conf
import sni.time as time
from sni.scheduler import scheduler
import sni.uac.user as user


class TeamspeakAuthenticationChallenge(me.Document):
    """
    Represents a teamspeak authentication challenge, akin to
    :class:`sni.uac.token.StateCode`.

    See also:
        :meth:`sni.teamspeak.new_authentication_challenge`
    """
    created_on = me.DateTimeField(default=time.now, required=True)
    user = me.ReferenceField(user.User, required=True, unique=True)
    challenge_nickname = me.StringField(required=True, unique=True)
    meta = {
        'indexes': [
            {
                'fields': ['created_on'],
                'expireAfterSeconds': 60,
            },
        ],
    }


class TeamspeakClient(pydantic.BaseModel):
    """
    Represents a teamspeak client as reported by the teamspeak query server.
    """
    cid: int
    clid: int
    client_database_id: int
    client_nickname: str
    client_type: int


class TeamspeakUser(me.Document):
    """
    Represent a teamspeak user.
    """
    created_on = me.DateTimeField(default=time.now, required=True)
    teamspeak_id = me.IntField(required=True)
    user = me.ReferenceField(user.User, required=True, unique=True)


def client_list(connection: ts3.query.TS3Connection) -> List[TeamspeakClient]:
    """
    Returns the list of clients currently connected to the teamspeak server.

    See also:
        :class:`sni.teamspeak.TeamspeakClient`
    """
    return [TeamspeakClient(**raw) for raw in connection.clientlist()]


def complete_authentication_challenge(connection: ts3.query.TS3Connection,
                                      usr: user.User):
    """
    Complete an authentication challenge, see
    :meth:`sni.teamspeak.new_authentication_challenge`.
    """
    challenge: TeamspeakAuthenticationChallenge = TeamspeakAuthenticationChallenge.objects.get(
        user=usr)
    client = find_client(connection, nickname=challenge.challenge_nickname)
    TeamspeakUser.objects(user=usr).modify(
        new=True,
        set__teamspeak_id=client.client_database_id,
        set__user=usr,
        upsert=True,
    )
    challenge.delete()
    logging.info('Completed authentication challenge for %s',
                 usr.character_name)
    update_client(connection, client)


def find_client(connection: ts3.query.TS3Connection,
                *,
                nickname: Optional[str] = None,
                client_database_id: Optional[int] = None) -> TeamspeakClient:
    """
    Returns the :class:`sni.teamspeak.TeamspeakClient` representation if a
    client. Raises a :class:`LookupError` if the client is not found, or if
    multiple client with the same nickname are found.
    """
    clients = [
        client for client in client_list(connection)
        if client.client_nickname == nickname
        or client.client_database_id == client_database_id
    ]
    if len(clients) != 1:
        raise LookupError
    return clients[0]


def new_authentication_challenge(usr: user.User) -> str:
    """
    Initiates an authentication challenge. The challenge proceeds as follows:

    1. A user (:class:`sni.uac.user.User`) asks to start a challenge by calling
       this method.

    2. This methods returns a UUID, and the user has 60 seconds to change its
       teamspeak nickname to that UUID.

    3. The user notifies SNI that (s)he has done so.

    4. The server checks (see
       :meth:`sni.teamspeak.complete_authentication_challenge`), and if
       sucessful, the corresponding teamspeak client is registered in the
       database and bound to that user. The nickname is also automatically
       assigned.
    """
    logging.info('Starting authentication challenge for %s',
                 usr.character_name)
    challenge_nickname = ''.join([
        random.choice(string.ascii_letters + string.digits) for _ in range(20)
    ])
    challenge = TeamspeakAuthenticationChallenge(
        user=usr,
        challenge_nickname=challenge_nickname,
    ).save()
    return str(challenge.challenge_nickname)


def new_connection() -> ts3.query.TS3Connection:
    """
    Returns a new connection to the teamspeak server.
    """
    connection = ts3.query.TS3Connection(
        conf.get('teamspeak.host'),
        conf.get('teamspeak.port'),
    )
    connection.use(sid=conf.get('teamspeak.server_id'))
    connection.login(
        client_login_name=conf.get('teamspeak.username'),
        client_login_password=conf.get('teamspeak.password'),
    )
    logging.info(
        'Connected to teamspeak server %s:%d as %s',
        conf.get('teamspeak.host'),
        conf.get('teamspeak.port'),
        conf.get('teamspeak.username'),
    )
    return connection


def update_client(connection: ts3.query.TS3Connection,
                  client: TeamspeakClient):
    """
    Update's a teamspeak client data and permissions, if that client is
    registered as a teamspeak user.
    """
    tsusr: TeamspeakUser = TeamspeakUser.objects(
        teamspeak_id=client.client_database_id).first()
    if tsusr is not None:
        logging.debug(
            'Updating known teamspeak client %s (%d) bound to user %s',
            client.client_nickname, client.client_database_id,
            tsusr.user.character_name)
        connection.clientedit(clid=client.clid,
                              client_description=tsusr.user.tickered_name)
    else:
        logging.debug('Updating unknown teamspeak client %s (%d)',
                      client.client_nickname, client.client_database_id)


@scheduler.scheduled_job('interval', minutes=10)
def update_clients():
    """
    Updates all teamspeak clients. See :meth:`sni.teamspeak.update_client`.
    """
    logging.info('Updating all teamspeak clients')
    connection = new_connection()
    for client in client_list(connection):
        try:
            update_client(connection, client)
        except Exception as error:
            logging.error('Failed to update client %s (%d): %s',
                          client.client_nickname, client.client_database_id,
                          str(error))
