"""
Discord bot commands
"""

import logging

from discord import Member
from discord.ext.commands import Context

import sni.conf as conf
from sni.user.user import User

from .discord import complete_authentication_challenge
from .bot import bot
from .jobs import update_discord_user


@bot.command()
async def auth(ctx: Context, code: str):
    """
    Authentication command. See authentication challenges:
    :meth:`sni.discord.discord.new_authentication_challenge` and
    :meth:`sni.discord.discord.complete_authentication_challenge`
    """
    if ctx.channel.id != conf.get('discord.auth_channel_id'):
        return
    member: Member = ctx.author
    try:
        complete_authentication_challenge(member, code)
        usr: User = User.objects(discord_user_id=member.id).get()
        await update_discord_user(usr)
        await ctx.message.delete()
    except Exception as error:
        logging.error('Could not authenticate Discord user %d: %s',
                      ctx.author.id, str(error))
