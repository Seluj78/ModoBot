import logging

import discord

from modobot import modobot_client
from modobot.static import ARCHIVE_CHANNEL_ID
from modobot.utils.france_datetime import clean_format
from modobot.utils.france_datetime import datetime_now_france


async def send_archive(actionlog):
    logging.info("Preparing to send archive")
    logging.debug("Getting channel")
    channel = modobot_client.get_channel(int(ARCHIVE_CHANNEL_ID))
    logging.debug("Preparing embed")
    embed = discord.Embed(
        title=f"**Case {str(actionlog.id)} | {str(actionlog.action).capitalize()} | {actionlog.user_name}**",
        color=discord.Color.magenta(),
    )
    embed.add_field(
        name="Membre",
        value=actionlog.user_name if actionlog.action != "unban" else actionlog.user_id,
        inline=True,
    )
    embed.add_field(name="Moderateur", value=actionlog.moderator_name, inline=True)
    if actionlog.action in ["ban", "warn", "note"]:
        embed.add_field(name="Raison", value=actionlog.comments, inline=True)
    elif actionlog.action == "mute":
        embed.add_field(
            name="Durée",
            value=str(actionlog.comments).split("(jusqu'à ")[-1].split(")")[0],
            inline=True,
        )
        embed.add_field(
            name="Raison", value=str(actionlog.comments).split("(jusqu'à ")[0]
        )
    embed.set_footer(
        text=f"ID: {actionlog.user_id} • {clean_format(datetime_now_france())}"
    )
    logging.debug("Sending archive embed")
    await channel.send(embed=embed)
