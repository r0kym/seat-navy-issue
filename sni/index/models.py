"""
Database models
"""

import mongoengine as me

from sni.user.models import User
import sni.utils as utils


class EsiCharacterLocation(me.Document):
    """
    Represents a character location, along with the ship it is currently
    flying. Thus, it is a combination of the ESI
    ``/characters/{character_id}/location``,
    ``/characters/{character_id}/online``, and
    ``/characters/{character_id}/ship`` paths.
    """

    online = me.BooleanField()
    """Wether the character is online"""

    ship_item_id = me.IntField()
    """Ship item ID (this ID persists until repackaged)"""

    ship_name = me.StringField()
    """Ship name"""

    ship_type_id = me.IntField()
    """Ship type ID"""

    solar_system_id = me.IntField()
    """Solar system ID where the character is"""

    station_id = me.IntField(null=True)
    """Station ID, if applicable"""

    structure_id = me.IntField(null=True)
    """Structire ID, if applicable"""

    timestamp = me.DateTimeField(default=utils.now)
    """Timestamp"""

    user = me.ReferenceField(User)
    """Corresponding user"""

    meta = {
        'index': [
            'online',
            ('user', '-timestamp'),
            ('solar_system_id', '-timestamp'),
            {
                'fields': ['timestamp'],
                'expireAfterSeconds': 3600 * 24 * 90,  # 90 days
            },
        ],
    }


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


class EsiWalletBalance(me.Document):
    """
    Represents a user's wallet balance at a given point in time
    """

    balance = me.FloatField()
    """Wallet balance"""

    timestamp = me.DateTimeField(default=utils.now)
    """Timestamp"""

    user = me.ReferenceField(User)
    """User reference"""

    meta = {
        'index': [
            ('user', '-timestamp'),
            {
                'fields': ['timestamp'],
                'expireAfterSeconds': 3600 * 24 * 90,  # 90 days
            },
        ],
    }
