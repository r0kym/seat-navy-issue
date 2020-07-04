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
from ts3.query import TS3Connection, TS3QueryError

import sni.conf as conf
import sni.utils as utils
import sni.user.user as user
import sni.user.group as group


class TeamspeakAuthenticationChallenge(me.Document):
    """
    Represents a teamspeak authentication challenge, akin to
    :class:`sni.uac.token.StateCode`.

    See also:
        :meth:`sni.teamspeak.new_authentication_challenge`
    """
    created_on = me.DateTimeField(default=utils.now, required=True)
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


class TeamspeakGroup(pydantic.BaseModel):
    """
    Represents a teamspeak group as reported by the teamspeak query server.
    """
    iconid: int
    name: str
    savedb: int
    sgid: int
    type: int


def client_list(connection: TS3Connection) -> List[TeamspeakClient]:
    """
    Returns the list of clients currently connected to the teamspeak server.

    See also:
        :class:`sni.teamspeak.TeamspeakClient`
    """
    return [TeamspeakClient(**raw) for raw in connection.clientlist()]


def complete_authentication_challenge(connection: TS3Connection,
                                      usr: user.User):
    """
    Complete an authentication challenge, see
    :meth:`sni.teamspeak.new_authentication_challenge`.
    """
    challenge: TeamspeakAuthenticationChallenge = TeamspeakAuthenticationChallenge.objects.get(
        user=usr)
    client = find_client(connection, nickname=challenge.challenge_nickname)
    usr.teamspeak_cldbid = client.client_database_id
    usr.save()
    auth_group = group.ensure_autogroup(conf.get('teamspeak.auth_group_name'))
    auth_group.modify(add_to_set__members=usr)
    challenge.delete()
    logging.info('Completed authentication challenge for %s',
                 usr.character_name)


def ensure_group(connection: TS3Connection, name: str) -> TeamspeakGroup:
    """
    Ensures that a teamspeak group exists, and returns a
    :class:`sni.teamspeak.teamspeak.TeamspeakGroup`.
    """
    try:
        return find_group(connection, name=name)
    except LookupError:
        connection.servergroupadd(name=name)
        logging.debug('Created Teamspeak group %s', name)
        return find_group(connection, name=name)


def find_client(connection: TS3Connection,
                *,
                nickname: Optional[str] = None,
                client_database_id: Optional[int] = None) -> TeamspeakClient:
    """
    Returns the :class:`sni.teamspeak.TeamspeakClient` representation of a
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


def find_group(connection: TS3Connection,
               *,
               name: Optional[str] = None,
               group_id: Optional[int] = None) -> TeamspeakGroup:
    """
    Returns the :class:`sni.teamspeak.TeamspeakGroup` representation of a
    teamspeak group. Raises a :class:`LookupError` if the group is not found.
    """
    groups = [
        grp for grp in group_list(connection)
        if grp.sgid == group_id or grp.name == name
    ]
    if len(groups) != 1:
        raise LookupError
    return groups[0]


def group_list(connection: TS3Connection) -> List[TeamspeakGroup]:
    """
    Returns the list of groups in the teamspeak server.

    See also:
        :class:`sni.teamspeak.TeamspeakGroup`
    """
    return [TeamspeakGroup(**raw) for raw in connection.servergrouplist()]


def new_authentication_challenge(usr: user.User) -> str:
    """
    Initiates an authentication challenge. The challenge proceeds as follows:

    1. A user (:class:`sni.user.user.User`) asks to start a challenge by calling
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


def new_connection() -> TS3Connection:
    """
    Returns a new connection to the teamspeak server.
    """
    connection = TS3Connection(
        conf.get('teamspeak.host'),
        conf.get('teamspeak.port'),
    )
    connection.use(sid=conf.get('teamspeak.server_id'))
    connection.login(
        client_login_name=conf.get('teamspeak.username'),
        client_login_password=conf.get('teamspeak.password'),
    )
    try:
        connection.clientupdate(client_nickname=conf.get('teamspeak.bot_name'))
    except TS3QueryError:
        pass
    logging.info(
        'Connected to teamspeak server %s:%d as %s',
        conf.get('teamspeak.host'),
        conf.get('teamspeak.port'),
        conf.get('teamspeak.username'),
    )
    return connection