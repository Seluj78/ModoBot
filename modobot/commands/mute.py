import contextlib
import json
import logging
from typing import Optional

import discord
from discord.utils import sleep_until

from modobot import modobot_client
from modobot.models.actionlog import ActionLog
from modobot.models.usermute import UserMute
from modobot.utils.archive import send_archive
from modobot.utils.converters import BaseMember
from modobot.utils.converters import TimeConverter
from modobot.utils.errors import AlreadyMuteError
from modobot.utils.errors import NotMutedError
from modobot.utils.france_datetime import clean_format
from modobot.utils.france_datetime import datetime_now_france


@modobot_client.command(brief="Mute un membre durant la durée donnée")
async def mute(
    ctx,
    member: BaseMember,
    dt_unmute: Optional[TimeConverter] = None,
    *,
    reason: Optional[str] = None,
):
    logging.debug("Deleting source message")
    await ctx.message.delete()

    try:
        logging.debug("Trying to get if user is already muted")
        UserMute.select().where(
            (UserMute.muted_id == member.id) & (UserMute.is_unmuted == False)  # noqa
        ).order_by(UserMute.id.desc()).get()
    except UserMute.DoesNotExist:
        pass
    else:
        logging.warning("user is already muted")
        raise AlreadyMuteError("Cet utilisateur est déjà mute.")

    user_roles = []
    logging.debug("Removing roles")
    for role in member.roles[1:]:
        logging.debug(f"Removing role {role.name}")
        user_roles.append(role.id)
        await member.remove_roles(role)

    for role in ctx.guild.roles:
        if role.name == "Muted":
            break
    if not role:
        raise ValueError("Role 'Muted' not found")
    logging.debug("Adding role Muted")
    await member.add_roles(role)

    if not reason:
        reason = "Pas de raison donnée"

    logging.debug("Creating mute in database")
    new_mute = UserMute.create(
        muted_id=member.id,
        moderator_id=ctx.author.id,
        reason=reason,
        dt_unmute=dt_unmute,
        user_roles=json.dumps(user_roles),
    )

    logging.debug("Creating action log in mute")
    new_log = ActionLog.create(
        moderator_name=str(ctx.author),
        moderator_id=ctx.author.id,
        user_name=str(member),
        user_id=member.id,
        action="mute",
        comments=reason + f"(jusqu'à {clean_format(dt_unmute)})",
    )

    logging.debug("Creating user mute embed")
    embed = discord.Embed(
        description=f":shushing_face: Vous avez été mute de `{ctx.guild.name}`.",
        color=discord.Color.dark_purple(),
    )
    embed.add_field(name="Raison", value=reason)
    embed.add_field(
        name="Jusqu'à",
        value=clean_format(dt_unmute) if dt_unmute is not None else "Indéfiniment",
    )
    embed.set_footer(text=f"Action effectuée le {clean_format(datetime_now_france())}")
    with contextlib.suppress(discord.Forbidden):
        logging.debug("Sending user mute embed")
        await member.send(embed=embed)

    logging.debug("Creating mute channel embed")
    embed = discord.Embed(
        description=f":shushing_face: `{str(member)}` (`{member.id}`) à été **mute**.",
        color=discord.Color.dark_purple(),
    )
    embed.add_field(name="Raison", value=f"`{reason}`.")
    embed.add_field(
        name="Jusqu'à",
        value=clean_format(dt_unmute) if dt_unmute is not None else "Indéfiniment",
    )
    embed.set_footer(text=f"Action effectuée le {clean_format(datetime_now_france())}")
    logging.debug("Sending channel mute embed")
    await ctx.channel.send(embed=embed)
    logging.debug("Sending mute archive")
    await send_archive(new_log)

    if dt_unmute:
        logging.debug(f"Sleeping until {dt_unmute}")
        await sleep_until(dt_unmute)
        logging.debug("Removing role 'Muted'")
        await member.remove_roles(role)
        logging.debug("Adding roles back")
        for role_id in user_roles:
            role = ctx.guild.get_role(role_id)
            logging.debug(f"Adding role {role.name}")
            await member.add_roles(role)

        logging.debug("Setting unmute in database")
        new_mute.is_unmuted = True
        new_mute.dt_unmuted = datetime_now_france()
        new_mute.save()

        logging.debug("Creating action log for unmute")
        new_log = ActionLog.create(
            moderator_name="automatic",
            moderator_id=0,
            user_name=str(member),
            user_id=member.id,
            action="unmute",
        )

        logging.debug("Creating user embed for unmute")
        embed = discord.Embed(
            description=f":raised_hands: Vous avez été **unmute** de `{ctx.guild.name}`.",
            color=discord.Color.green(),
        )
        embed.set_footer(
            text=f"Action effectuée le {clean_format(datetime_now_france())}"
        )
        with contextlib.suppress(discord.Forbidden):
            logging.debug("Sending user unmute embed")
            await member.send(embed=embed)
        logging.debug("Sending unmute archive")
        await send_archive(new_log)


@modobot_client.command(brief="Démute un membre")
async def unmute(ctx, member: discord.Member):
    logging.debug("Deleting source message")
    await ctx.message.delete()
    for role in ctx.guild.roles:
        if role.name == "Muted":
            break
    if not role:
        raise ValueError("Role 'Muted' not found")
    logging.debug("Removing 'Muted' role")
    await member.remove_roles(role)

    logging.debug("Getting last mute for user")
    last_mute = (
        UserMute.select()
        .where(UserMute.muted_id == member.id)
        .order_by(UserMute.id.desc())
        .get()
    )
    if last_mute.is_unmuted:
        logging.warning("User is not muted")
        raise NotMutedError("L'utilisateur n'est pas mute")
    logging.debug("Setting as unmuted in DB")
    last_mute.is_unmuted = True
    last_mute.dt_unmuted = datetime_now_france()
    last_mute.save()

    logging.debug("Adding roles back")
    for role_id in json.loads(last_mute.user_roles):
        role = ctx.guild.get_role(role_id)
        logging.debug(f"Adding role {role.name}")
        await member.add_roles(role)

    logging.debug("Creating action log for unmute")
    new_log = ActionLog.create(
        moderator_name=str(ctx.author),
        moderator_id=ctx.author.id,
        user_name=str(member),
        user_id=member.id,
        action="unmute",
    )
    logging.debug("Creating user unmute embed")
    embed = discord.Embed(
        description=f":raised_hands: Vous avez été **unmute** de `{ctx.guild.name}`.",
        color=discord.Color.green(),
    )
    embed.set_footer(text=f"Action effectuée le {clean_format(datetime_now_france())}")
    with contextlib.suppress(discord.Forbidden):
        logging.debug("Sending user unmute embed")
        await member.send(embed=embed)

    logging.debug("Creating channel unmute embed")
    embed = discord.Embed(
        description=f"`{str(member)}` (`{member.id}`) à été **unmute**.",
        color=discord.Color.green(),
    )
    embed.set_footer(text=f"Action effectuée le {clean_format(datetime_now_france())}")
    logging.debug("Sending channel unmute embed")
    await ctx.channel.send(embed=embed)
    logging.debug("Sending unmute archive")
    await send_archive(new_log)
