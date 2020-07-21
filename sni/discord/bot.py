"""
Discord Bot management. The bot requires the ``bot`` scope, and the following
permissions:

* ``Manage Roles``
* ``Change Nickname``
* ``Manage Nicknames``
* ``Send Messages``
* ``Manage Messages``

which corresponds to the the permission integer ``469772288``. Therefore, the
invitation link for the bot should look like this:
``https://discord.com/api/oauth2/authorize?client_id=<bot_id>&permissions=469772288&scope=bot``.

See also: `Discord developer portal
    <https://discord.com/developers/applications>`_, `Creating a Bot Account
    <https://discordpy.readthedocs.io/en/latest/discord.html#discord-intro>`_
"""

import asyncio
import logging

from discord.ext.commands import Bot
import discord

import sni.conf as conf

JOBS_KEY: str = 'scheduler.discord.jobs'
"""The redis key for the job list"""

RUN_TIMES_KEY: str = 'scheduler.discord.run_times'
"""The redis key for the job run times"""

bot = Bot(
    command_prefix='!',
    description='SeAT Navy Issue Discord Bot',
    event_loop=asyncio.get_event_loop(),
)


def get_guild() -> discord.Guild:
    """
    Returns a guild handler corresponding to the ``discord.server_id`` setting.
    """
    return bot.get_guild(conf.get('discord.server_id'))


def get_member(user_id: int) -> discord.Member:
    """
    Gets a guild member by its user ID.
    """
    return get_guild().get_member(user_id)


async def log(message: str):
    """
    Sends a message on the logging channel. If configuration key
    ``discord.log_channel_id`` is ``None``, does't do anything.
    """
    log_channel_id = conf.get('discord.log_channel_id')
    if log_channel_id is None:
        return
    log_channel = bot.get_channel(log_channel_id)
    await log_channel.send(message)


async def start_bot():
    """
    Runs the discord client in a different thread.
    """
    logging.info('Starting Discord client')
    await bot.start(conf.get('discord.token'))
