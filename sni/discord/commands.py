"""
Discord bot commands
"""

import logging

from discord import Member
from discord.ext.commands import Context

from sni.conf import CONFIGURATION as conf
from sni.user.models import User

from .discord import complete_authentication_challenge
from .bot import bot, log
from .jobs import update_discord_user


@bot.command()
async def auth(ctx: Context, code: str):
    """
    Starts a Discord authentication challenge.
    """
    if ctx.channel.id != conf.discord.auth_channel_id:
        return
    member: Member = ctx.author
    try:
        complete_authentication_challenge(member, code)
        usr: User = User.objects(discord_user_id=member.id).get()
        await update_discord_user(usr)
        logging.info(
            "Successfully authenticated user %s (%d)",
            ctx.author.name,
            ctx.author.id,
        )
        await ctx.channel.send(
            f"Hi <@{ctx.author.id}> :wave:, you are now authenticated. "
            "Welcome aboard!"
        )
        await log(
            f":white_check_mark: Successfully authenticated <@{ctx.author.id}>"
        )
    except Exception as error:
        logging.error(
            "Could not authenticate Discord user %s (%d): %s",
            ctx.author.name,
            ctx.author.id,
            str(error),
        )
        await ctx.channel.send(
            f":x: Sorry <@{ctx.author.id}>, I could not authenticate you. "
            "Please try again with a different code. If the problem persists, "
            "contact your Discord administrator."
        )
        await log(
            f":x: Failed to authenticate <@{ctx.author.id}>: {str(error)}"
        )
    await ctx.message.delete()
