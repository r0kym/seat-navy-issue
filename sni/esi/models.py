"""
ESI related database models
"""

import mongoengine as me

import sni.utils as utils
from sni.user.models import User


class EsiAccessToken(me.Document):
    """
    A model representing an ESI access token, along with its refresh token and
    relevant metadatas.
    """
    access_token = me.StringField(required=True)
    created_on = me.DateTimeField(required=True, default=utils.now)
    expires_on = me.DateTimeField(required=True)
    owner = me.ReferenceField(User,
                              required=True,
                              reverse_delete_rule=me.DO_NOTHING)
    scopes = me.ListField(me.StringField(), required=True, default=[])
    meta = {
        'indexes': [
            {
                'fields': ['expires_on'],
                'expireAfterSeconds': 0,
            },
        ],
    }


class EsiPath(me.Document):
    """
    Represents a path in ESI's openapi specification.

    See also:
        `EVE Swagger Interface <https://esi.evetech.net/ui>`_
        `EVE Swagger Interface (JSON) <https://esi.evetech.net/latest/swagger.json>`_
    """
    http_method = me.StringField(required=True)
    path_re = me.StringField(required=True)
    path = me.StringField(required=True, unique_with='http_method')
    scope = me.StringField(required=False)
    version = me.StringField(required=True)


class EsiRefreshToken(me.Document):
    """
    A model representing an ESI access token, along with its refresh token and
    relevant metadatas.
    """
    created_on = me.DateTimeField(required=True, default=utils.now)
    updated_on = me.DateTimeField(required=True, default=utils.now)
    owner = me.ReferenceField(User,
                              required=True,
                              reverse_delete_rule=me.DO_NOTHING)
    refresh_token = me.StringField(required=True)
    scopes = me.ListField(me.StringField(), required=True, default=[])
