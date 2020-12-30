import contextlib
import logging

import discord

from modobot import modobot_client
from modobot.models.actionlog import ActionLog
from modobot.models.guildsettings import GuildSettings
from modobot.models.userwarn import UserWarn
from modobot.utils.archive import send_archive
from modobot.utils.converters import BaseMember
from modobot.utils.france_datetime import clean_format
from modobot.utils.france_datetime import datetime_now_france


@modobot_client.command(brief="Avertis un utilisateur")
async def warn(ctx, member: BaseMember, *, reason: str):
    logging.debug("Deleting source message")
    await ctx.message.delete()

    logging.debug("Creating warn embed")
    embed = discord.Embed(
        description=f":warning: Vous avez été **avertis** dans `{ctx.guild.name}`.",
        color=discord.Color.orange(),
    )
    embed.add_field(name="Raison", value=reason)
    with contextlib.suppress(discord.Forbidden):
        logging.debug("Sending embed to warned used")
        await member.send(embed=embed)

    guildsettings = GuildSettings.get(GuildSettings.guild_id == ctx.guild.id)

    logging.debug("Creating warn in DB")
    UserWarn.create(
        warned_id=member.id,
        warned_name=str(member),
        moderator_id=ctx.author.id,
        moderator_name=str(ctx.author),
        reason=reason,
        guild=guildsettings,
    )
    logging.debug("Creating warn action log")
    new_log = ActionLog.create(
        moderator_name=str(ctx.author),
        moderator_id=ctx.author.id,
        user_name=str(member),
        user_id=member.id,
        action="warn",
        comments=reason,
        guild=guildsettings,
    )

    logging.debug("Creating warn channel embed")
    embed = discord.Embed(
        description=f":warning: `{str(member)}` (`{member.id}`) à été **averti**.",
        color=discord.Color.orange(),
    )
    embed.add_field(name="Raison", value=reason)
    embed.set_footer(text=f"Action effectuée le {clean_format(datetime_now_france())}")
    logging.debug("Sending warn channel embed")
    await ctx.channel.send(embed=embed)
    logging.debug("Sending warn archive")
    await send_archive(actionlog=new_log)
