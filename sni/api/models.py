"""
ESI related database models
"""

import mongoengine as me

import sni.utils as utils
from sni.user.models import User


class CrashReportRequest(me.EmbeddedDocument):
    """
    Represents a request made to the API.
    """
    # cookies = me.DictField(default=None)
    # hooks = me.DictField(default=None)
    # auth = me.DynamicField(default=None)
    # data = me.DynamicField(default=None, null=True)
    # files = me.DictField(default=None, null=True)
    headers = me.DictField(default=None, null=True)
    # json = me.DynamicField(default=None, null=True)
    method = me.StringField(default=None)
    params = me.DynamicField(default=None, null=True)
    url = me.StringField(default=None)

    def to_dict(self) -> dict:
        """
        Returns a dict representation
        """
        return {
            'headers': self.headers,
            'method': self.method,
            'params': self.params,
            'url': self.url,
        }


class CrashReportToken(me.EmbeddedDocument):
    """
    Represents a token in a crash report
    """
    created_on = me.DateTimeField()
    expires_on = me.DateTimeField()
    owner = me.ReferenceField(User)
    token_type = me.StringField()
    uuid = me.UUIDField()

    def to_dict(self) -> dict:
        """
        Returns a dict representation
        """
        return {
            'created_on': str(self.created_on),
            'expires_on': str(self.expires_on),
            'owner': {
                'authorized_to_login': self.owner.authorized_to_login,
                'character_id': self.owner.character_id,
                'character_name': self.owner.character_name,
                'clearance_level': self.owner.clearance_level,
                'created_on': str(self.owner.created_on),
                'updated_on': str(self.owner.updated_on),
            },
            'token_type': self.token_type,
            'uuid': str(self.uuid),
        }


class CrashReport(me.Document):
    """
    Information about a crash, i.e. an uncaught exception that occured during
    an API request processing. (in fact, the exception is still cought by
    :meth:`sni.api.server.exception_handler` as a last resort, and this is
    where this class is used to save traces to the database).
    """
    SCHEMA_VERSION = 1

    _version = me.IntField(default=SCHEMA_VERSION, required=True)
    request = me.EmbeddedDocumentField(CrashReportRequest, required=True)
    timestamp = me.DateTimeField(default=utils.now, required=True)
    trace = me.ListField(me.StringField())
    token = me.EmbeddedDocumentField(CrashReportToken, null=True)

    meta = {
        'indexes': [
            '-timestamp',
            {
                'fields': ['timestamp'],
                'expireAfterSeconds': 3600 * 24 * 90,  # 90 days
            }
        ]
    }

    def to_dict(self) -> dict:
        """
        Returns a dict representation
        """
        return {
            'id': str(self.pk),
            'request': self.request.to_dict(),
            'timestamp': str(self.timestamp),
            'token': self.token.to_dict(),
            'trace': self.trace,
        }
