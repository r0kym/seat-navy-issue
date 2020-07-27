"""
Teamspeak database models
"""

import mongoengine as me

from sni.user.models import User
import sni.utils as utils


class TeamspeakAuthenticationChallenge(me.Document):
    """
    Represents a teamspeak authentication challenge, akin to
    :class:`sni.uac.token.StateCode`.

    See also:
        :meth:`sni.teamspeak.new_authentication_challenge`
    """

    created_on = me.DateTimeField(default=utils.now, required=True)
    """Timestamp of the creation of this document"""

    user = me.ReferenceField(User, required=True, unique=True)
    """"Corresponding user"""

    challenge_nickname = me.StringField(required=True, unique=True)
    """See :meth:`sni.teamspeak.teamspeak.new_authentication_challenge`"""

    meta = {
        'indexes': [
            {
                'fields': ['created_on'],
                'expireAfterSeconds': 60,
            },
        ],
    }