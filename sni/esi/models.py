"""
ESI related database models
"""

import mongoengine as me

from sni.esi.scope import EsiScope
from sni.user.models import User
import sni.utils as utils


class EsiPath(me.Document):
    """
    Represents a path in ESI's openapi specification.

    See also:
        `EVE Swagger Interface <https://esi.evetech.net/ui>`_
        `EVE Swagger Interface (JSON) <https://esi.evetech.net/latest/swagger.json>`_
    """

    http_method = me.StringField(required=True)
    """HTTP method"""

    path_re = me.StringField(required=True)
    """Regular expression for this path, in string form"""

    path = me.StringField(required=True, unique_with="http_method")
    """String form of the path, e.g. ``/characters/{character_id}/``"""

    scope = me.StringField(choices=EsiScope, required=False)
    """Scope required for this path"""

    version = me.StringField(required=True)
    """ESI version (NOT schema version)"""


class EsiRefreshToken(me.Document):
    """
    A model representing an ESI access token, along with its refresh token and
    relevant metadatas.
    """

    SCHEMA_VERSION = 2
    """Latest schema version for this collection"""

    _version = me.IntField(default=SCHEMA_VERSION, required=True)
    """Schema version of this document"""

    created_on = me.DateTimeField(required=True, default=utils.now)
    """Timestamp of the creation of this document"""

    updated_on = me.DateTimeField(required=True, default=utils.now)
    """Timestamp of the last update of this document"""

    owner = me.ReferenceField(
        User, required=True, reverse_delete_rule=me.DO_NOTHING
    )
    """Reference to the owner of this token"""

    refresh_token = me.StringField(required=True)
    """The ESI refresh token string"""

    scopes = me.ListField(
        me.StringField(choices=EsiScope), required=True, default=[]
    )
    """ESI scopes of the refresh token"""

    valid = me.BooleanField(default=True)
    """Wether this refresh token is valid"""

    meta = {
        "indexes": ["valid", ("owner", "scopes", "valid"),],
    }


class EsiAccessToken(me.Document):
    """
    A model representing an ESI access token, along with its refresh token and
    relevant metadatas.
    """

    SCHEMA_VERSION = 2
    """Latest schema version for this collection"""

    _version = me.IntField(default=SCHEMA_VERSION, required=True)
    """Schema version of this document"""

    access_token = me.StringField(required=True)
    """The ESI access token string"""

    created_on = me.DateTimeField(required=True, default=utils.now)
    """Timestamp of the creation of this access token (according to the ESI)"""

    expires_on = me.DateTimeField(required=True)
    """Expiration timestamp of this access token (according to the ESI)"""

    owner = me.ReferenceField(
        User, required=True, reverse_delete_rule=me.DO_NOTHING
    )
    """Reference to the owner of this token"""

    refresh_token = me.ReferenceField(
        EsiRefreshToken, reverse_delete_rule=me.CASCADE
    )
    """Reference towards the refresh token that issued this access token"""

    scopes = me.ListField(
        me.StringField(choices=EsiScope), required=True, default=[]
    )
    """ESI scopes of the access token"""

    meta = {
        "indexes": [{"fields": ["expires_on"], "expireAfterSeconds": 0,},],
    }
