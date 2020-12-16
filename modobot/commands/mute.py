import datetime
import re

import discord
from discord.utils import sleep_until

from modobot import modobot_client
from modobot.models.actionlog import ActionLog
from modobot.models.usermute import UserMute
from modobot.utils.errors import IncorrectTimeError
from modobot.utils.france_datetime import datetime_now_france


@modobot_client.command(brief="Mute un membre durant la durée donnée")
async def mute(ctx, member: discord.Member, time: str, *, reason: str):
    await ctx.message.delete()
    for role in ctx.guild.roles:
        if role.name == "Muted":
            break
    if not role:
        raise ValueError("Role 'Muted' not found")
    await member.add_roles(role)

    matches = re.fullmatch("(\d+)([mhd])", time)  # noqa
    if not matches:
        raise IncorrectTimeError("Doit être `0000m/h/d`")
    count = int(matches[1])
    s_type = matches[2]

    if s_type == "m":
        delta = datetime.timedelta(minutes=count)
    elif s_type == "h":
        delta = datetime.timedelta(hours=count)
    elif s_type == "d":
        delta = datetime.timedelta(days=count)
    else:
        raise IncorrectTimeError("Doit être `0000m/h/d`")

    dt_unmute = datetime_now_france() + delta

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
        comments=reason + f"(pour {time})",
    )

    embed = discord.Embed(
        description=f"Vous avez été mute de `{ctx.guild.name}`.",
        color=discord.Color.red(),
    )
    embed.add_field(name="Raison", value=reason)
    embed.add_field(name="Jusqu'à", value=datetime_now_france() + delta)
    await member.send(embed=embed)

    embed = discord.Embed(
        description=f"`{str(member)}` (`{member.id}`) à été mute.",
        color=discord.Color.dark_purple(),
    )
    embed.add_field(name="Raison", value=f"`{reason}`.")
    embed.add_field(name="Jusqu'à", value=f"`{datetime_now_france() + delta}`.")
    embed.set_footer(
        text=f"Depuis la commande `{ctx.command.name}` envoyée par {str(ctx.author)} dans #{ctx.channel.name}"
    )
    await ctx.channel.send(embed=embed)

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

    ActionLog.create(
        moderator="automatic", user=f"{str(member)} ({member.id})", action="unmute"
    )

    embed = discord.Embed(
        description=f"Vous avez été unmute de `{ctx.guild.name}`.",
        color=discord.Color.red(),
    )
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

    ActionLog.create(
        moderator=f"{ctx.author.id} ({str(ctx.author)})",
        user=f"{str(member)} ({member.id})",
        action="unmute",
    )

    embed = discord.Embed(
        description=f"Vous avez été unmute de `{ctx.guild.name}`.",
        color=discord.Color.red(),
    )
    await member.send(embed=embed)

    embed = discord.Embed(
        description=f"`{str(member)}` (`{member.id}`) à été démute.",
        color=discord.Color.dark_purple(),
    )
    embed.set_footer(
        text=f"Depuis la commande `{ctx.command.name}` envoyée par {str(ctx.author)} dans #{ctx.channel.name}"
    )
    await ctx.channel.send(embed=embed)
