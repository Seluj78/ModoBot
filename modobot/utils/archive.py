import logging

import discord

from modobot import modobot_client
from modobot.utils.france_datetime import clean_format
from modobot.utils.france_datetime import datetime_now_france


async def send_archive(actionlog):
    logging.info("Preparing to send archive")
    logging.debug("Getting channel")
    channel = modobot_client.get_channel(actionlog.guild.archive_channel_id)
    logging.debug("Preparing embed")

    emoji_dict = {
        "lock": "⛔",
        "unlock": "▶️",
        "clear": "🧹",
        "mute": "🤫",
        "unmute": "🗣",
        "ban": "💀",
        "unban": "👋",
        "note": "🗒",
        "search": "🔎",
        "warn": "⚠️",
    }

    if actionlog.action == "clear":
        channel_id = actionlog.comments.split(" ")[3]
        size = actionlog.comments.split(" ")[1]
        embed = discord.Embed(
            title=f"** Action {str(actionlog.id)} | {emoji_dict.get(actionlog.action, '❔')} "
            f"{str(actionlog.action).capitalize()} **",
            color=discord.Color.magenta(),
        )
        embed.add_field(name="Channel", value=f"<#{channel_id}>", inline=True)
        embed.add_field(name="Size", value=size, inline=True)
        embed.add_field(name="Modérateur", value=actionlog.moderator_name, inline=True)
        embed.set_footer(
            text=f"💬 ID: {channel_id} • 🕐 {clean_format(datetime_now_france())}"
        )
    elif actionlog.action in ["lock", "unlock"]:
        channel_id = actionlog.comments.split(" ")[1]
        embed = discord.Embed(
            title=f"** Action {str(actionlog.id)} | {emoji_dict.get(actionlog.action, '❔')} "
            f"{str(actionlog.action).capitalize()} **",
            color=discord.Color.magenta(),
        )
        embed.add_field(name="Channel", value=f"<#{channel_id}>", inline=True)
        embed.add_field(name="Modérateur", value=actionlog.moderator_name, inline=True)
        embed.set_footer(
            text=f"💬 ID: {channel_id} • 🕐 {clean_format(datetime_now_france())}"
        )
    else:
        member = (
            actionlog.user_name if actionlog.action != "unban" else actionlog.user_id
        )
        embed = discord.Embed(
            title=f"**Case {str(actionlog.id)} | {emoji_dict.get(actionlog.action, '❔')} "
            f"{str(actionlog.action).capitalize()} | {member}**",
            color=discord.Color.magenta(),
        )
        embed.add_field(name="Membre", value=member, inline=True)
        embed.add_field(name="Modérateur", value=actionlog.moderator_name, inline=True)
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
            text=f"👤 ID: {actionlog.user_id} • 🕐 {clean_format(datetime_now_france())}"
        )
    logging.debug("Sending archive embed")
    await channel.send(embed=embed)
