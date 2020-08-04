"""
Models
"""

from enum import Enum

import mongoengine as me

from sni.user.models import Corporation, User
import sni.utils as utils


class Token(me.Document):
    """
    Represents a token issued by SNI.
    """

    class TokenType(str, Enum):
        """
        Enumeration containing the various token types.
        """

        dyn = "dyn"  # Dynamic app token
        per = "per"  # Permanent app token
        use = "use"  # User token

    callback = me.URLField(default=None, null=True)
    """Callback URL of the application. When a new user token is issued, the
    corresponding application is notified at this URL."""

    comments = me.StringField(default=str)
    """Comments"""

    created_on = me.DateTimeField(default=utils.now, required=True)
    """Timestamp of the creation of this document"""

    expires_on = me.DateTimeField(default=None, null=True)
    """Self explanatory"""

    owner = me.ReferenceField(
        User, required=True, reverse_delete_rule=me.CASCADE
    )
    """Reference to the owner of this token"""

    parent = me.ReferenceField(
        "self", default=None, null=True, reverse_delete_rule=me.CASCADE
    )
    """Optional reference to the token that has been used to create this one"""

    token_type = me.StringField(choices=TokenType, required=True)
    """Token type, see :class:`sni.uac.models.Token.TokenType`"""

    uuid = me.UUIDField(binary=False, unique=True)
    """
    UUID of this token

    Todo:
        Use the document's ``_id`` field instead.
    """

    meta = {
        "indexes": [{"fields": ["expires_on"], "expireAfterSeconds": 0,},],
    }


class StateCode(me.Document):
    """
    Represents a state code and related metadatas.

    A state code is issued when a new user token is issued from a dynamic app
    token, and is a way for SNI to remeber about the authentication while the
    end user logs in to EVE SSO.
    """

    SCHEMA_VERSION = 2
    """Latest schema version for this collection"""

    _version = me.IntField(default=SCHEMA_VERSION)
    """Schema version of this document"""

    app_token = me.ReferenceField(Token, required=True)
    """The app token that created this state code"""

    created_on = me.DateTimeField(default=utils.now, required=True)
    """Timestamp of the creation of this document"""

    inviting_corporation = me.ReferenceField(
        Corporation, default=None, null=True, required=False
    )
    """Corporation inviting the user of that state code, if any"""

    uuid = me.UUIDField(binary=False, unique=True)
    """
    The state code

    Todo:
        Use the document's ``_id`` field instead.
    """

    meta = {
        "indexes": [{"fields": ["created_on"], "expireAfterSeconds": 600,},],
    }
