import logging

import discord

from modobot import modobot_client
from modobot.models.actionlog import ActionLog
from modobot.models.guildsettings import GuildSettings
from modobot.models.userban import UserBan
from modobot.models.usernote import UserNote
from modobot.models.userwarn import UserWarn
from modobot.utils.archive import send_archive
from modobot.utils.france_datetime import clean_format
from modobot.utils.france_datetime import datetime_now_france


@modobot_client.command(brief="Recherche dans la DB sur un utilisateur")
async def search(ctx, member: discord.Member):
    logging.debug("Deleting source message")
    await ctx.message.delete()

    guildsettings = GuildSettings.get(GuildSettings.guild_id == ctx.guild.id)

    logging.debug("Creating action log for search")
    new_log = ActionLog.create(
        moderator_name=str(ctx.author),
        moderator_id=ctx.author.id,
        user_name=str(member),
        user_id=member.id,
        action="search",
        comments=member.id,
        guild=guildsettings,
    )
    logging.debug(f"Getting notes, warns, bans for userc {member.id}")
    notes = UserNote.select().where(UserNote.noted_id == member.id)
    warns = UserWarn.select().where(UserWarn.warned_id == member.id)
    bans = UserBan.select().where(UserBan.banned_id == member.id)

    logging.debug("Creating search embed")
    embed = discord.Embed(
        description=f":mag_right: **{str(member)}** (`{member.id}`)",
        color=discord.Color.blue(),
    )
    top_role = member.top_role
    user_joined = member.joined_at
    embed.add_field(
        name="Status de l'utilisateur",
        value=f"Rejoins le {user_joined}\nGrade le plus haut : {top_role}",
    )
    if notes:
        msg = """"""
        for note in notes:
            moderator = modobot_client.get_user(int(note.moderator_id))
            msg += f"{str(moderator)} à noté `{note.reason}` le {note.dt_noted}\n--------\n"
        embed.add_field(name="Notes", value=msg, inline=False)
    if warns:
        msg = """"""
        for warn in warns:
            moderator = modobot_client.get_user(int(warn.moderator_id))
            msg += f"{str(moderator)} à averti `{warn.reason}` le {warn.dt_warned}\n--------\n"
        embed.add_field(name="Warns", value=msg, inline=False)
    if bans:
        msg = """"""
        for ban in bans:
            moderator = modobot_client.get_user(int(ban.moderator_id))
            msg += f"{str(moderator)} à banni avec comme raison `{ban.reason}` le {ban.dt_banned}"
            if ban.is_unbanned:
                msg += f" (débanni le {ban.dt_unbanned})\n--------\n"
            else:
                msg += "\n"
        embed.add_field(name="Bans", value=msg, inline=False)
    embed.set_footer(text=f"Action effectuée le {clean_format(datetime_now_france())}")

    logging.debug("Sending search embed")
    await ctx.channel.send(embed=embed)
    logging.debug("Sending search archive")
    await send_archive(actionlog=new_log)
