"""
Discord related functionalities
"""

import logging

import discord
import mongoengine as me

from sni.user.models import User
import sni.utils as utils


class DiscordAuthenticationChallenge(me.Document):
    """
    Represents a pending authentication challenge.
    """
    code = me.StringField(required=True, unique=True)
    created_on = me.DateTimeField(default=utils.now, required=True)
    user = me.ReferenceField(User, required=True, unique=True)
    meta = {
        'indexes': [
            {
                'fields': ['created_on'],
                'expireAfterSeconds': 60,
            },
        ],
    }


def complete_authentication_challenge(discord_user: discord.User, code: str):
    """
    Complete an authentication challenge, see
    :meth:`sni.discord.discord.new_authentication_challenge`.
    """
    challenge = DiscordAuthenticationChallenge.objects(code=code).get()
    usr = challenge.user
    usr.discord_user_id = discord_user.id
    usr.save()
    logging.info('Authenticated Discord user %d to user %s', discord_user.id,
                 usr.tickered_name)
    challenge.delete()


def new_authentication_challenge(usr: User) -> str:
    """
    Creates a new authentication challenge.

    The challenge proceeds as follows:

    1. A user (:class:`sni.user`) asks to start a challenge by
       calling this method.

    2. This methods returns a random code, and the user has 60 seconds type
       ``!auth <code>`` in the dedicated authentication channel.

    3. The Discord client is notified, and check this code against the pending
       Discort authentication challenges.
    """
    logging.info('Starting Discord authentication challenge for %s',
                 usr.character_name)
    challenge = DiscordAuthenticationChallenge(
        user=usr,
        code=utils.random_code(50),
    ).save()
    return challenge.code
