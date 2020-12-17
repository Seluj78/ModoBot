import discord

from modobot import modobot_client
from modobot.static import ARCHIVE_CHANNEL_ID
from modobot.utils.france_datetime import datetime_now_france


async def send_archive(actionlog):
    channel = modobot_client.get_channel(int(ARCHIVE_CHANNEL_ID))
    embed = discord.Embed(
        title=f"**Case {str(actionlog.id)} | {str(actionlog.action).capitalize()} | {actionlog.user_name}**"
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
    embed.set_footer(text=f"ID: {actionlog.user_id} • {datetime_now_france()}")
    await channel.send(embed=embed)
