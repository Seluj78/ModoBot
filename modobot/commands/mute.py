import contextlib
from typing import Optional

import discord
from discord.utils import sleep_until

from modobot import modobot_client
from modobot.models.actionlog import ActionLog
from modobot.models.usermute import UserMute
from modobot.utils.converters import BaseMember
from modobot.utils.converters import TimeConverter
from modobot.utils.errors import AlreadyMuteError
from modobot.utils.france_datetime import datetime_now_france


@modobot_client.command(brief="Mute un membre durant la durée donnée")
async def mute(
    ctx,
    member: BaseMember,
    dt_unmute: Optional[TimeConverter] = None,
    *,
    reason: Optional[str] = None,
):
    await ctx.message.delete()

    try:
        UserMute.select().where(
            (UserMute.muted_id == member.id) & (UserMute.is_unmuted == False)  # noqa
        ).order_by(UserMute.id.desc()).get()
    except UserMute.DoesNotExist:
        pass
    else:
        raise AlreadyMuteError("Cet utilisateur est déjà mute.")

    for role in ctx.guild.roles:
        if role.name == "Muted":
            break
    if not role:
        raise ValueError("Role 'Muted' not found")
    await member.add_roles(role)

    if not reason:
        reason = "Pas de raison donnée"

    UserMute.create(
        muted_id=member.id,
        moderator_id=ctx.author.id,
        reason=reason,
        dt_unmute=dt_unmute,
    )

    ActionLog.create(
        moderator=f"{ctx.author.id} ({str(ctx.author)})",
        user=f"{str(member)} ({member.id})",
        action="mute",
        comments=reason + f"(jusqu'à {dt_unmute})",
    )

    embed = discord.Embed(
        description=f":shushing_face: Vous avez été mute de `{ctx.guild.name}`.",
        color=discord.Color.red(),
    )
    embed.add_field(name="Raison", value=reason)
    embed.add_field(
        name="Jusqu'à", value=dt_unmute if dt_unmute is not None else "Indéfiniment"
    )
    embed.set_footer(text=f"Action effectuée le {datetime_now_france()}")
    with contextlib.suppress(discord.Forbidden):
        await member.send(embed=embed)

    embed = discord.Embed(
        description=f":shushing_face: `{str(member)}` (`{member.id}`) à été **mute**.",
        color=discord.Color.dark_purple(),
    )
    embed.add_field(name="Raison", value=f"`{reason}`.")
    embed.add_field(
        name="Jusqu'à",
        value=f"`{dt_unmute if dt_unmute is not None else 'Indéfiniment'}`.",
    )
    embed.set_footer(text=f"Action effectuée le {datetime_now_france()}")
    await ctx.channel.send(embed=embed)

    if dt_unmute:
        await sleep_until(dt_unmute)
        await member.remove_roles(role)

        last_mute = (
            UserMute.select()
            .where(UserMute.muted_id == member.id)
            .order_by(UserMute.id.desc())
            .get()
        )
        last_mute.is_unmuted = True
        last_mute.dt_unmuted = datetime_now_france()
        last_mute.save()

        ActionLog.create(
            moderator="automatic", user=f"{str(member)} ({member.id})", action="unmute"
        )

        embed = discord.Embed(
            description=f":raised_hands: Vous avez été **unmute** de `{ctx.guild.name}`.",
            color=discord.Color.green(),
        )
        embed.set_footer(text=f"Action effectuée le {datetime_now_france()}")
        with contextlib.suppress(discord.Forbidden):
            await member.send(embed=embed)


@modobot_client.command(brief="Démute un membre")
async def unmute(ctx, member: discord.Member):
    await ctx.message.delete()
    for role in ctx.guild.roles:
        if role.name == "Muted":
            break
    if not role:
        raise ValueError("Role 'Muted' not found")
    await member.remove_roles(role)

    last_mute = (
        UserMute.select()
        .where(UserMute.muted_id == member.id)
        .order_by(UserMute.id.desc())
        .get()
    )
    last_mute.is_unmuted = True
    last_mute.dt_unmuted = datetime_now_france()
    last_mute.save()

    ActionLog.create(
        moderator=f"{ctx.author.id} ({str(ctx.author)})",
        user=f"{str(member)} ({member.id})",
        action="unmute",
    )

    embed = discord.Embed(
        description=f":raised_hands: Vous avez été **unmute** de `{ctx.guild.name}`.",
        color=discord.Color.green(),
    )
    embed.set_footer(text=f"Action effectuée le {datetime_now_france()}")
    with contextlib.suppress(discord.Forbidden):
        await member.send(embed=embed)

    embed = discord.Embed(
        description=f"`{str(member)}` (`{member.id}`) à été **unmute**.",
        color=discord.Color.dark_purple(),
    )
    embed.set_footer(text=f"Action effectuée le {datetime_now_france()}")
    await ctx.channel.send(embed=embed)
