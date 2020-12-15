from datetime import datetime

import discord

from modobot import modobot_client
from modobot.models.actionlog import ActionLog
from modobot.models.userban import UserBan
from modobot.utils.errors import UserAlreadyBannedError
from modobot.utils.errors import UserNotBannedError


@modobot_client.command(brief="Bans a member with the given reason")
async def ban(ctx, member: discord.Member, *, reason: str):

    if not member or member == ctx.message.author:
        await ctx.message.delete()
        embed = discord.Embed(
            description="You cannot ban yourself.", color=discord.Color.dark_orange()
        )
        await ctx.author.send(embed=embed)
        return
    if UserBan.get_or_none(banned_id=member.id, is_unbanned=False):
        raise UserAlreadyBannedError(f"User {str(member)} is already banned")

    embed = discord.Embed(
        description=f"You were banned from `{ctx.guild.name}`.",
        color=discord.Color.red(),
    )
    embed.add_field(name="Reason", value=reason)
    await member.send(embed=embed)

    await member.ban(reason=reason)
    UserBan.create(banned_id=member.id, moderator_id=ctx.author.id, reason=reason)
    ActionLog.create(
        moderator_id=ctx.author.id, user_id=member.id, action="ban", comments=reason
    )

    await ctx.message.delete()
    embed = discord.Embed(
        description=f"`{str(member)}` (`{member.id}`) was banned.",
        color=discord.Color.red(),
    )
    embed.add_field(name="Reason", value=f"`{reason}`.")
    embed.set_footer(
        text=f"From command `{ctx.command.name}` sent by {str(ctx.author.name)} in #{ctx.channel.name}"
    )
    await ctx.channel.send(embed=embed)


@modobot_client.command(brief="Unbans a member")
async def unban(ctx, *, member_id: str):
    banned_user = UserBan.get_or_none(banned_id=member_id, is_unbanned=False)
    if not banned_user:
        raise UserNotBannedError(f"User {member_id} is not banned.")

    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        if str(ban_entry.user.id) == str(member_id):
            await ctx.guild.unban(ban_entry.user)
            banned_user.is_unbanned = True
            banned_user.dt_unbanned = datetime.utcnow()
            banned_user.save()
            ActionLog.create(
                moderator_id=ctx.author.id, user_id=member_id, action="unban"
            )

            await ctx.message.delete()
            embed = discord.Embed(
                description=f"`{member_id}` was unbanned.",
                color=discord.Color.dark_gold(),
            )
            embed.set_footer(
                text=f"From command `{ctx.command.name}` sent by {str(ctx.author.name)} in #{ctx.channel.name}"
            )
            await ctx.channel.send(embed=embed)
            return
    raise UserNotBannedError(f"User {member_id} is not banned.")
