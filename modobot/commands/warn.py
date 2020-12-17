import contextlib

import discord

from modobot import modobot_client
from modobot.models.actionlog import ActionLog
from modobot.models.userwarn import UserWarn
from modobot.utils.archive import send_archive
from modobot.utils.converters import BaseMember
from modobot.utils.france_datetime import datetime_now_france


@modobot_client.command(brief="Avertis un utilisateur")
async def warn(ctx, member: BaseMember, *, reason: str):
    await ctx.message.delete()

    embed = discord.Embed(
        description=f":warning: Vous avez été **avertis** dans `{ctx.guild.name}`.",
        color=discord.Color.orange(),
    )
    embed.add_field(name="Raison", value=reason)
    with contextlib.suppress(discord.Forbidden):
        await member.send(embed=embed)

    UserWarn.create(warned_id=member.id, moderator_id=ctx.author.id, reason=reason)
    new_log = ActionLog.create(
        moderator_name=str(ctx.author),
        moderator_id=ctx.author.id,
        user_name=str(member),
        user_id=member.id,
        action="warn",
        comments=reason,
    )

    embed = discord.Embed(
        description=f":warning: `{str(member)}` (`{member.id}`) à été **averti**.",
        color=discord.Color.orange(),
    )
    embed.add_field(name="Raison", value=reason)
    embed.set_footer(text=f"Action effectuée le {datetime_now_france()}")
    await ctx.channel.send(embed=embed)
    await send_archive(actionlog=new_log)
