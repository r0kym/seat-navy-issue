"""
Database models
"""

import mongoengine as me

ESIMAIL_SCHEMA_VERSION = 1


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
    _version = me.IntField(default=ESIMAIL_SCHEMA_VERSION)
    body = me.StringField()
    from_id = me.IntField()
    mail_id = me.IntField()
    recipients = me.EmbeddedDocumentListField(EsiMailRecipient)
    subject = me.StringField()
    timestamp = me.DateTimeField()
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
