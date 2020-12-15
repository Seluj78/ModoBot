import discord

from modobot import modobot_client
from modobot.models.actionlog import ActionLog
from modobot.models.userwarn import UserWarn


@modobot_client.command(brief="Warns a member with given reason")
async def warn(ctx, member: discord.Member, *, reason: str):
    await ctx.message.delete()
    if not member or member == ctx.message.author:
        embed = discord.Embed(
            description="You cannot warn yourself.", color=discord.Color.dark_orange()
        )
        await ctx.author.send(embed=embed)
        return

    embed = discord.Embed(
        description=f"You were warned in `{ctx.guild.name}`.",
        color=discord.Color.orange(),
    )
    embed.add_field(name="Reason", value=reason)
    await member.send(embed=embed)

    UserWarn.create(warned_id=member.id, moderator_id=ctx.author.id, reason=reason)
    ActionLog.create(
        moderator_id=ctx.author.id, user_id=member.id, action="warn", comments=reason
    )

    embed = discord.Embed(
        description=f"`{str(member)}` (`{member.id}`) was warned.",
        color=discord.Color.orange(),
    )
    embed.add_field(name="Reason", value=f"`{reason}`.")
    embed.set_footer(
        text=f"From command `{ctx.command.name}` sent by {str(ctx.author.name)} in #{ctx.channel.name}"
    )
    await ctx.channel.send(embed=embed)
