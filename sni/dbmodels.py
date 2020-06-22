"""
Database models

Reference:
    `MongoEngine User Documentation <http://docs.mongoengine.org/index.html>`_
"""

from enum import Enum

from mongoengine import (
    CASCADE,
    DateTimeField,
    Document,
    IntField,
    ListField,
    ReferenceField,
    StringField,
    URLField,
    UUIDField,
)

import sni.time as time


class User(Document):
    """
    User model.

    A user corresponds to a single EVE character. A user can reference other
    users as "sub characters".
    """
    character_id = IntField(unique=True)
    character_name = StringField(required=True)
    created_on = DateTimeField(required=True, default=time.now)
    subcharacter_ids = ListField(IntField(), default=[])


class Token(Document):
    """
    Represents a token issued by SNI.
    """
    class TokenType(str, Enum):
        """
        Enumeration containing the various token types.
        """
        dyn = 'dyn'  # Dynamic app token
        per = 'per'  # Permanent app token
        use = 'use'  # User token

    callback = URLField(default=None)
    comments = StringField()
    created_on = DateTimeField(required=True, default=time.now)
    expires_on = DateTimeField(null=True, default=None)
    owner = ReferenceField(User, required=True, reverse_delete_rule=CASCADE)
    parent = ReferenceField('self',
                            null=True,
                            default=None,
                            reverse_delete_rule=CASCADE)
    token_type = StringField(choices=TokenType, required=True)
    uuid = UUIDField(binary=False, unique=True)


class StateCode(Document):
    """
    Represents a state code and related metadatas.

    A state code is issued when a new user token is issued from a dynamic app
    token, and is a way for SNI to remeber about the authentication while the
    end user logs in to EVE SSO.
    """
    app_token = ReferenceField(Token, required=True)
    created_on = DateTimeField(required=True, default=time.now)
    uuid = UUIDField(binary=False, unique=True)
