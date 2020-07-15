"""
Database models
"""

import mongoengine as me

from sni.user.models import User
import sni.utils as utils


class EsiMailRecipient(me.EmbeddedDocument):
    """
    An email recipient
    """
    recipient_id = me.IntField()
    recipient_type = me.StringField()


class EsiMail(me.Document):
    """
    Represents a EVE mail. This collection has a text search index on the
    ``body`` and ``subject`` fields (see `here
    <http://docs.mongoengine.org/guide/text-indexes.html>`_)
    """
    SCHEMA_VERSION = 1
    """Latest schema version for this collection"""

    _version = me.IntField(default=SCHEMA_VERSION)
    """Schema version of this document"""

    body = me.StringField()
    """Body of the email"""

    from_id = me.IntField()
    """Character id of the sender"""

    mail_id = me.IntField()
    """Mail id (according to the ESI)"""

    recipients = me.EmbeddedDocumentListField(EsiMailRecipient)
    """Recipient list. See :class:`sni.index.models.EsiMailRecipient`."""

    subject = me.StringField()
    """Subject of the email"""

    timestamp = me.DateTimeField()
    """ESI timestamp of the email"""

    meta = {
        'indexes': [
            {
                'default_language': 'english',
                'fields': ['$body', '$subject'],
                'weights': {
                    'body': 10,
                    'subject': 2
                },
            },
        ]
    }


class EsiSkillPoints(me.Document):
    """
    Represents a measurment of a character's skill points
    """
    SCHEMA_VERSION = 1
    """Latest schema version for this collection"""

    _version = me.IntField(default=SCHEMA_VERSION)
    """Schema version of this document"""

    timestamp = me.DateTimeField(default=utils.now)
    """Timestamp of this skillpoint measurment"""

    total_sp = me.IntField()
    """Total skillpoints"""

    unallocated_sp = me.IntField()
    """Unallocated skillpoints"""

    user = me.ReferenceField(User)
    """Corresponding user"""

    meta = {
        'index': [
            ('user', '-timestamp'),
            {
                'fields': ['timestamp'],
                'expireAfterSeconds': 3600 * 24 * 90,  # 90 days
            },
        ],
    }
