import logging

import discord

from modobot import modobot_client
from modobot.models.actionlog import ActionLog
from modobot.utils.france_datetime import datetime_now_france


@modobot_client.command(brief="Verrouille un channel")
async def lock(ctx, channel: discord.TextChannel = None):
    logging.debug("Deleting source message")
    await ctx.message.delete()

    channel = channel or ctx.channel
    logging.debug("Creating action log")
    ActionLog.create(
        moderator_name=str(ctx.author),
        moderator_id=ctx.author.id,
        action="lock",
        comments=f"Locked {str(channel)}",
    )

    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False

    logging.debug("Overwriting permissions for users")
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

    logging.debug("Creating lock embed")
    embed = discord.Embed(
        description=f":no_entry: Canal `{channel}` **verrouillé**.",
        color=discord.Color.red(),
    )
    embed.set_footer(text=f"Action effectuée le {datetime_now_france()}")
    logging.debug("Sending lock embed")
    await ctx.channel.send(embed=embed)


@modobot_client.command(brief="Déverrouille un channel")
async def unlock(ctx, channel: discord.TextChannel = None):
    logging.debug("Deleting source message")
    await ctx.message.delete()

    channel = channel or ctx.channel

    logging.debug("Creating action log for unlock")
    ActionLog.create(
        moderator_name=str(ctx.author),
        moderator_id=ctx.author.id,
        action="unlock",
        comments=f"Unlocked {str(channel)}",
    )

    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True

    logging.debug("Overwriting permissions for users")
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    logging.debug("Creating unlock embed")
    embed = discord.Embed(
        description=f":arrow_forward: Canal `{channel}` **déverouillé**",
        color=discord.Color.green(),
    )
    embed.set_footer(text=f"Action effectuée le {datetime_now_france()}")
    logging.debug("Sending unlock embed")
    await ctx.channel.send(embed=embed)
