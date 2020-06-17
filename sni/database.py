"""
Database layer

Reference:
    `MongoEngine User Documentation <http://docs.org/index.html>`_
"""

import logging
from uuid import uuid4

import jwt
from mongoengine import (
    CASCADE,
    connect,
    DateTimeField,
    DO_NOTHING,
    Document,
    IntField,
    ListField,
    ReferenceField,
    StringField,
    UUIDField,
)

import sni.conf as conf
import sni.time as time


class User(Document):
    """
    User model.

    A user corresponds to a single EVE character. A user can reference other
    users as "sub characters".
    """
    character_id = IntField(primary_key=True)
    character_name = StringField(required=True)
    created_on = DateTimeField(required=True)
    subcharacter_ids = ListField(IntField(), default=[])


class Token(Document):
    """
    Represents a token issued by SNI.
    """
    TOKEN_TYPES = [
        'dyn',  # Dynamic app token
        'per',  # Permanent app token
        'use',  # User token
    ]
    created_on = DateTimeField(required=True)
    expires_on = DateTimeField(null=True, default=None)
    owner = ReferenceField(User, required=True, reverse_delete_rule=CASCADE)
    token_type = StringField(choices=TOKEN_TYPES, required=True)
    uuid = UUIDField(primary_key=True)

    def to_jwt(self) -> str:
        """
        Derives a JWT token byte array from the current token.
        """
        return jwt.encode(
            {
                'created_on': str(self.created_on),
                'expires_on': str(self.expires_on),
                'owner': self.owner.character_id,
                'token_type': self.token_type,
                'uuid': str(self.uuid),
            },
            conf.get('jwt.secret'),
            algorithm=conf.get('jwt.algorithm'),
        ).decode()


class EsiToken(Document):
    """
    A model representing an ESI access token, along with its refresh token and
    relevant metadatas.
    """
    access_token = StringField(required=True)
    app_token = ReferenceField(Token, reverse_delete_rule=CASCADE)
    created_on = DateTimeField(required=True)
    expires_on = DateTimeField(required=True)
    owner = ReferenceField(User, required=True, reverse_delete_rule=DO_NOTHING)
    refresh_token = StringField(required=True)
    scopes = ListField(StringField, required=True, default=[])


def init():
    """
    Connects to the MongoDB instance.

    Does not return anything. Any call to ``mongoengine`` will act on that
    connection. It's magic.
    """
    connect(
        conf.get('database.database'),
        authentication_source=conf.get('database.authentication_source'),
        host=conf.get('database.host'),
        password=conf.get('database.password'),
        port=conf.get('database.port'),
        username=conf.get('database.username'),
    )
    query_set = User.objects(character_id=0)
    if query_set.count() == 0:
        root = User(
            character_id=0,
            character_name='root',
            created_on=time.now(),
        )
        root.save()
        logging.info('Created root user')
    else:
        root = query_set.first()
    if Token.objects(owner=root, token_type='per').count() == 0:
        root_per_token = Token(
            created_on=time.now(),
            owner=root,
            token_type='per',
            uuid=uuid4(),
        )
        root_per_token.save()
        logging.info('No permanent app token owned by root, created one: %s',
                     root_per_token.to_jwt())
    if Token.objects(owner=root, token_type='dyn').count() == 0:
        root_dyn_token = Token(
            created_on=time.now(),
            owner=root,
            token_type='dyn',
            uuid=uuid4(),
        )
        root_dyn_token.save()
        logging.info('No dynamic app token owned by root, created one: %s',
                     root_dyn_token.to_jwt())
