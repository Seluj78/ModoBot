import discord

from modobot import modobot_client
from modobot.models.actionlog import ActionLog
from modobot.models.userwarn import UserWarn


@modobot_client.command(brief="Avertis un utilisateur")
async def warn(ctx, member: discord.Member, *, reason: str):
    await ctx.message.delete()
    if not member or member == ctx.message.author:
        embed = discord.Embed(
            description="Vous ne pouvez pas vous avertir vous même. :eyes:",
            color=discord.Color.dark_orange(),
        )
        await ctx.author.send(embed=embed)
        return

    embed = discord.Embed(
        description=f"Vous avez été avertis dans `{ctx.guild.name}`.",
        color=discord.Color.orange(),
    )
    embed.add_field(name="Raison", value=reason)
    await member.send(embed=embed)

    UserWarn.create(warned_id=member.id, moderator_id=ctx.author.id, reason=reason)
    ActionLog.create(
        moderator=f"{str(ctx.author)} ({ctx.author.id})",
        user=f"{str(member)} ({member.id})",
        action="warn",
        comments=reason,
    )

    embed = discord.Embed(
        description=f"`{str(member)}` (`{member.id}`) à été averti.",
        color=discord.Color.orange(),
    )
    embed.add_field(name="Raison", value=f"`{reason}`.")
    embed.set_footer(
        text=f"Depuis la commande `{ctx.command.name}` envoyée par {str(ctx.author.name)} dans #{ctx.channel.name}"
    )
    await ctx.channel.send(embed=embed)
