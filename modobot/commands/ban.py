import contextlib
import logging

import discord

from modobot import modobot_client
from modobot.models.actionlog import ActionLog
from modobot.models.guildsettings import GuildSettings
from modobot.models.userban import UserBan
from modobot.static import SERVER_URL
from modobot.utils.archive import send_archive
from modobot.utils.converters import BaseMember
from modobot.utils.errors import UserAlreadyBannedError
from modobot.utils.errors import UserNotBannedError
from modobot.utils.france_datetime import clean_format
from modobot.utils.france_datetime import datetime_now_france


@modobot_client.command(brief="Ban un membre avec la raison donnée")
async def ban(ctx, member: BaseMember, *, reason: str):
    logging.debug("Deleting source message")
    await ctx.message.delete()
    if UserBan.get_or_none(banned_id=member.id, is_unbanned=False):
        logging.warning("User is already banned")
        raise UserAlreadyBannedError(f"L'utilisateur {str(member)} est déjà banni.")

    guildsettings = GuildSettings.get(GuildSettings.guild_id == ctx.guild.id)

    logging.debug("Creating ban in database")
    new_ban = UserBan.create(
        banned_id=member.id,
        banned_name=str(member),
        moderator_id=ctx.author.id,
        moderator_name=str(ctx.author),
        reason=reason,
        guild=guildsettings,
    )

    logging.debug("Creating user ban embed")
    embed = discord.Embed(
        description=f"💀 Vous avez été **banni** de `{ctx.guild.name}`.",
        color=discord.Color.red(),
    )
    embed.add_field(name="Raison", value=reason)
    embed.add_field(
        name="Vous souhaitez faire appel ?",
        value=f"Clickez sur le lien et suivez les instructions\n{SERVER_URL + '/appeal/' + str(new_ban.id)}",
    )
    embed.set_footer(text=f"Action effectuée le {clean_format(datetime_now_france())}")
    with contextlib.suppress(discord.Forbidden):
        logging.debug("Sending user ban embed")
        await member.send(embed=embed)

    logging.debug("Banning member")
    await member.ban(reason=reason)

    logging.debug("Creating action log for ban")
    new_log = ActionLog.create(
        moderator_name=str(ctx.author),
        moderator_id=ctx.author.id,
        user_name=str(member),
        user_id=member.id,
        action="ban",
        comments=reason,
        guild=guildsettings,
    )

    logging.debug("Creating channel embed for ban")
    embed = discord.Embed(
        description=f"💀 `{str(member)}` (`{member.id}`) à été **banni**.",
        color=discord.Color.red(),
    )
    embed.add_field(name="Raison", value=reason)
    embed.set_footer(text=f"Action effectuée le {clean_format(datetime_now_france())}")
    logging.debug("Sending channel embed for ban")
    await ctx.channel.send(embed=embed)
    logging.debug("Sending ban archive")
    await send_archive(actionlog=new_log)


@modobot_client.command(brief="Débanne un utilisateur")
async def unban(ctx, *, member_id: str):
    logging.debug("Deleting source message")
    await ctx.message.delete()
    guildsettings = GuildSettings.get(GuildSettings.guild_id == ctx.guild.id)

    banned_user = UserBan.get_or_none(
        banned_id=member_id, is_unbanned=False, guild=guildsettings
    )
    if not banned_user:
        logging.debug("User was not banned")
        raise UserNotBannedError(f"L'utilisateur {member_id} n'est pas banni.")

    logging.debug("Unbanning user")
    await ctx.guild.unban(discord.Object(id=member_id))
    logging.debug("Setting ban db to unbanned")
    banned_user.is_unbanned = True
    banned_user.dt_unbanned = datetime_now_france()
    banned_user.save()
    logging.debug("Creating action log for unban")
    new_log = ActionLog.create(
        moderator_name=str(ctx.author),
        moderator_id=ctx.author.id,
        user_id=member_id,
        action="unban",
        guild=guildsettings,
    )
    logging.debug("Creating channel unban embed")
    embed = discord.Embed(
        description=f":wave: `{member_id}` à été **pardonné** (unban).",
        color=discord.Color.green(),
    )
    embed.set_footer(text=f"Action effectuée le {clean_format(datetime_now_france())}")
    logging.debug("Sending channel unban emebed")
    await ctx.channel.send(embed=embed)
    logging.debug("Sending unban archive")
    await send_archive(actionlog=new_log)
