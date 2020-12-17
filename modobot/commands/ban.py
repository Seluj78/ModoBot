import contextlib

import discord

from modobot import modobot_client
from modobot.models.actionlog import ActionLog
from modobot.models.userban import UserBan
from modobot.utils.archive import send_archive
from modobot.utils.converters import BaseMember
from modobot.utils.errors import UserAlreadyBannedError
from modobot.utils.errors import UserNotBannedError
from modobot.utils.france_datetime import datetime_now_france


@modobot_client.command(brief="Ban un membre avec la raison donnée")
async def ban(ctx, member: BaseMember, *, reason: str):
    await ctx.message.delete()
    if UserBan.get_or_none(banned_id=member.id, is_unbanned=False):
        raise UserAlreadyBannedError(f"L'utilisateur {str(member)} est déjà banni.")

    embed = discord.Embed(
        description=f":skull_crossbones: Vous avez été **banni** de `{ctx.guild.name}`.",
        color=discord.Color.red(),
    )
    embed.add_field(name="Raison", value=reason)
    embed.set_footer(text=f"Action effectuée le {datetime_now_france()}")
    with contextlib.suppress(discord.Forbidden):
        await member.send(embed=embed)

    await member.ban(reason=reason)
    UserBan.create(banned_id=member.id, moderator_id=ctx.author.id, reason=reason)
    new_log = ActionLog.create(
        moderator_name=str(ctx.author),
        moderator_id=ctx.author.id,
        user_name=str(member),
        user_id=member.id,
        action="ban",
        comments=reason,
    )

    embed = discord.Embed(
        description=f":skull_crossbones: `{str(member)}` (`{member.id}`) à été **banni**.",
        color=discord.Color.red(),
    )
    embed.add_field(name="Raison", value=reason)
    embed.set_footer(text=f"Action effectuée le {datetime_now_france()}")
    await ctx.channel.send(embed=embed)
    await send_archive(actionlog=new_log)


@modobot_client.command(brief="Débanne un utilisateur")
async def unban(ctx, *, member_id: str):
    await ctx.message.delete()

    banned_user = UserBan.get_or_none(banned_id=member_id, is_unbanned=False)
    if not banned_user:
        raise UserNotBannedError(f"L'utilisateur {member_id} n'est pas banni.")

    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        if str(ban_entry.user.id) == str(member_id):
            await ctx.guild.unban(ban_entry.user)
            banned_user.is_unbanned = True
            banned_user.dt_unbanned = datetime_now_france()
            banned_user.save()
            new_log = ActionLog.create(
                moderator_name=str(ctx.author),
                moderator_id=ctx.author.id,
                user_id=member_id,
                action="unban",
            )
            embed = discord.Embed(
                description=f":wave: `{member_id}` à été **pardonné** (unban).",
                color=discord.Color.dark_gold(),
            )
            embed.set_footer(text=f"Action effectuée le {datetime_now_france()}")
            await ctx.channel.send(embed=embed)
            await send_archive(actionlog=new_log)
            return
    raise UserNotBannedError(f"L'utilisateur {member_id} n'est pas banni.")
