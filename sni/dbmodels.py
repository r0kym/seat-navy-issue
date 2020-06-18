"""
Database models

Reference:
    `MongoEngine User Documentation <http://docs.mongoengine.org/index.html>`_
"""

from mongoengine import (
    CASCADE,
    DateTimeField,
    DO_NOTHING,
    Document,
    IntField,
    ListField,
    ReferenceField,
    StringField,
    UUIDField,
)


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
    parent = ReferenceField('self',
                            null=True,
                            default=None,
                            reverse_delete_rule=CASCADE)
    token_type = StringField(choices=TOKEN_TYPES, required=True)
    uuid = UUIDField(binary=False, primary_key=True)


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
