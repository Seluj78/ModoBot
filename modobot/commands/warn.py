import discord

from modobot import modobot_client
from modobot.models.actionlog import ActionLog
from modobot.models.userwarn import UserWarn


@modobot_client.command(brief="Warns a member with given reason")
async def warn(ctx, member: discord.Member, *, reason: str):

    if not member or member == ctx.message.author:
        await ctx.message.delete()
        await ctx.message.author.send("You cannot warn yourself")
        return

    embed = discord.Embed(
        title="Modobot notification",
        description=f"You were warned on {ctx.guild.name}",
        color=discord.Color.red(),
    )
    embed.add_field(name="Reason", value=reason, inline=True)
    await member.send(embed=embed)

    UserWarn.create(warned_id=member.id, moderator_id=ctx.author.id, reason=reason)
    await ctx.message.delete()
    await ctx.send(f"{ctx.author.id} warned {member.id} for {reason}")
    ActionLog.create(
        moderator_id=ctx.author.id, user_id=member.id, action="warn", comments=reason
    )
