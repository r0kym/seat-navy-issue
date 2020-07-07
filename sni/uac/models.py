"""
Models
"""

from enum import Enum

import mongoengine as me

from sni.user.models import User
import sni.utils as utils


class Token(me.Document):
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

    callback = me.URLField(default=None, null=True)
    comments = me.StringField(default=str)
    created_on = me.DateTimeField(default=utils.now, required=True)
    expires_on = me.DateTimeField(default=None, null=True)
    owner = me.ReferenceField(User,
                              required=True,
                              reverse_delete_rule=me.CASCADE)
    parent = me.ReferenceField('self',
                               default=None,
                               null=True,
                               reverse_delete_rule=me.CASCADE)
    token_type = me.StringField(choices=TokenType, required=True)
    uuid = me.UUIDField(binary=False, unique=True)
    meta = {
        'indexes': [
            {
                'fields': ['expires_on'],
                'expireAfterSeconds': 0,
            },
        ],
    }


class StateCode(me.Document):
    """
    Represents a state code and related metadatas.

    A state code is issued when a new user token is issued from a dynamic app
    token, and is a way for SNI to remeber about the authentication while the
    end user logs in to EVE SSO.
    """
    app_token = me.ReferenceField(Token, required=True)
    created_on = me.DateTimeField(default=utils.now, required=True)
    uuid = me.UUIDField(binary=False, unique=True)
    meta = {
        'indexes': [
            {
                'fields': ['created_on'],
                'expireAfterSeconds': 600,
            },
        ],
    }
