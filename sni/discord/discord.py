"""
Discord related functionalities
"""

import logging

import discord
import mongoengine as me

from sni.user.models import Group, User
import sni.utils as utils

from .bot import get_guild


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


async def ensure_role_for_group(grp: Group):
    """
    Ensure that a Discord role exists for the given group, and returns it.
    """
    if not grp.map_to_discord:
        return
    guild = get_guild()
    current_roles = {role.name: role for role in guild.roles}
    if grp.group_name in current_roles.keys():
        role = current_roles[grp.group_name]
    else:
        role = await guild.create_role(name=grp.group_name)
        grp.discord_role_id = role.id
        grp.save()
    return role


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
