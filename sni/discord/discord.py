"""
Discord module. The bot requires the ``bot`` scope, and the ``Manage Roles``,
``Change Nickname``, ``Manage Nicknames``, ``Send Messages`` permissions.

See also:
    `Creating a Bot Account <https://discordpy.readthedocs.io/en/latest/discord.html#discord-intro>`_
"""

import asyncio
import logging
from threading import Thread

from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import discord

import sni.conf as conf
import sni.utils as utils

client = discord.Client()
scheduler = AsyncIOScheduler(
    event_loop=client.loop,
    job_defaults={
        'coalesce': False,
        'executor': 'default',
        'jitter': '60',
        'jobstore': 'discord',
        'max_instances': 3,
        'misfire_grace_time': None,
    },
    jobstores={
        'discord': MemoryJobStore(),
    },
    timezone=utils.utc,
)


@client.event
async def on_disconnect():
    """
    Called when the Discord client has been disconnected. Executes cleanup
    tasks.
    """
    logging.info('Discord client disconnected')
    scheduler.shutdown()


@client.event
async def on_ready():
    """
    Called when the discord client is ready. Starts the discord client
    scheduler.
    """
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game('EVE Online'),
    )
    logging.info('Discord client online')
    scheduler.start()


def start():
    """
    Runs the discord client in a different thread.
    """
    async def _start():
        await client.start(conf.get('discord.token'))

    logging.info('Starting Discord client')
    client.loop.create_task(_start())
    thread = Thread(
        args=(client.loop, ),
        daemon=True,
        name='discord_client',
        target=asyncio.BaseEventLoop.run_forever,
    )
    thread.start()


start()
