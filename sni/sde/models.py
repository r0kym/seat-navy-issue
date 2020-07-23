"""
Teamspeak database models
"""

import mongoengine as me


class EsiObjectName(me.Document):
    """
    Represents an ID to object name mapping
    """

    SCHEMA_VERSION = 1
    """Latest schema version for this collection"""

    _version = me.IntField(default=SCHEMA_VERSION)
    """Schema version of this document"""

    expires_on = me.DateTimeField(default=None, null=True)
    """When this document expires, if applicable"""

    field_id = me.IntField(unique_with='field_names')
    """ID"""

    field_names = me.ListField(me.StringField())
    """ESI field names this type of field can have, e.g. ``solar_system_id``,
    ``character_id``"""

    name = me.StringField()
    """Name"""

    meta = {
        'index': [
            'field_id',
            ('field_names', 'field_id'),
            {
                'fields': ['expires_on'],
                'expireAfterSeconds': 0
            },
        ],
    }
