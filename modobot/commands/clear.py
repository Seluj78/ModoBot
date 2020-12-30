import logging

import discord

from modobot import modobot_client
from modobot.models.actionlog import ActionLog
from modobot.models.guildsettings import GuildSettings
from modobot.utils.france_datetime import clean_format
from modobot.utils.france_datetime import datetime_now_france


@modobot_client.command(brief="Supprime X messages dans le canal actuel")
async def clear(ctx, clear_size: int):
    logging.debug("Deleting source message")
    await ctx.message.delete()

    logging.debug(f"Clearing {clear_size} messages in {ctx.channel.name}")
    await ctx.channel.purge(limit=clear_size)
    guildsettings = GuildSettings.get(GuildSettings.guild_id == ctx.guild.id)

    logging.debug("Creating action log for clear")
    ActionLog.create(
        moderator_name=str(ctx.author),
        moderator_id=ctx.author.id,
        action="clear",
        comments=f"Cleared {clear_size}",
        guild=guildsettings,
    )
    channel = modobot_client.get_channel(guildsettings.archive_channel_id)
    logging.debug("Creating clear embed")
    embed = discord.Embed(
        description=f":wastebasket: **{clear_size} messages** on été supprimés dans `{ctx.channel.name}`",
        color=discord.Color.gold(),
    )
    embed.set_footer(text=f"Action effectuée le {clean_format(datetime_now_france())}")
    logging.debug("Sending clear embed")
    await channel.send(embed=embed)
