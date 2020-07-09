"""
Discord Bot management. The bot requires the ``bot`` scope, and the
``Manage Roles``, ``Change Nickname``, ``Manage Nicknames``, ``Send Messages``
permissions.

See also: `Creating a Bot Account
    <https://discordpy.readthedocs.io/en/latest/discord.html#discord-intro>`_
"""

import asyncio
import logging
from threading import Thread

from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot
import discord

import sni.conf as conf
import sni.utils as utils

bot = Bot(command_prefix='!', description='SeAT Navy Issue Discord Bot')

scheduler = AsyncIOScheduler(
    event_loop=bot.loop,
    job_defaults={
        'coalesce': True,
        'executor': 'default',
        'jitter': 60,
        'jobstore': 'discord',
        'max_instances': 3,
        'misfire_grace_time': None,
    },
    jobstores={
        'discord':
        RedisJobStore(db=conf.get('redis.database'),
                      host=conf.get('redis.host'),
                      jobs_key='scheduler.discord.jobs',
                      port=conf.get('redis.port'),
                      run_times_key='scheduler.discord.run_times'),
    },
    timezone=utils.utc,
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


def start():
    """
    Runs the discord client in a different thread.
    """
    async def _start():
        await bot.start(conf.get('discord.token'))

    logging.info('Starting Discord client')
    bot.loop.create_task(_start())
    thread = Thread(
        args=(bot.loop, ),
        daemon=True,
        name='discord_client',
        target=asyncio.BaseEventLoop.run_forever,
    )
    thread.start()
