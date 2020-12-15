from modobot import modobot_client
from modobot.utils.errors import UserAlreadyBannedError, UserNotBannedError
from modobot.models.userban import UserBan
import discord


@modobot_client.command()
async def ban(ctx, member: discord.Member, *, reason: str):
    if UserBan.get_or_none(banned_id=member.id):
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
    banned_user = UserBan.get_or_none(banned_id=member_id)
    if not banned_user:
        raise UserNotBannedError(f"User {member_id} is not banned.")

    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        if str(ban_entry.user.id) == str(member_id):
            await ctx.guild.unban(ban_entry.user)
            banned_user.delete_instance()
            await ctx.message.delete()
            await ctx.send(f"{ctx.author.id} unbanned {member_id}")
            return
    raise UserNotBannedError(f"User {member_id} is not banned.")
