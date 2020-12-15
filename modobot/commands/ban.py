import discord

from modobot import modobot_client
from modobot.models.userban import UserBan
from modobot.utils.errors import UserAlreadyBannedError
from modobot.utils.errors import UserNotBannedError
from datetime import datetime


@modobot_client.command()
async def ban(ctx, member: discord.Member, *, reason: str):

    if not member or member == ctx.message.author:
        await ctx.message.delete()
        await ctx.message.author.send("You cannot ban yourself")
        return

    if UserBan.get_or_none(banned_id=member.id, is_unbanned=False):
        raise UserAlreadyBannedError(f"User {str(member)} is already banned")

    embed = discord.Embed(
        title="Modobot notification",
        description=f"You were banned from {ctx.guild.name}",
        color=discord.Color.red(),
    )
    embed.add_field(name="Reason", value=reason, inline=True)
    await member.send(embed=embed)

    await member.ban(reason=reason)
    await ctx.message.delete()
    await ctx.send(f"{ctx.author.id} banned {member.id} for {reason}")
    UserBan.create(
        banned_id=member.id, moderator_id=ctx.author.id, reason=reason
    ).save()


@modobot_client.command()
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
            await ctx.message.delete()
            await ctx.send(f"{ctx.author.id} unbanned {member_id}")
            return
    raise UserNotBannedError(f"User {member_id} is not banned.")
