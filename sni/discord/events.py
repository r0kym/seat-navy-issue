"""
Discord events
"""

import logging

import discord

from .bot import bot, log, scheduler, start_scheduler


@bot.event
async def on_disconnect():
    """
    Called when the Discord client has been disconnected. Executes cleanup
    tasks.
    """
    logging.info('Discord client disconnected')
    scheduler.shutdown()


@bot.event
async def on_ready():
    """
    Called when the discord client is ready. Starts the discord client
    scheduler.
    """
    start_scheduler()
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game('EVE Online'),
    )
    logging.info('Discord client online')
    await log('SeAT Navy Issue online o7')
