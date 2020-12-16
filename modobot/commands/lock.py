import discord

from modobot import modobot_client
from modobot.models.actionlog import ActionLog


@modobot_client.command(brief="Verrouille un channel")
async def lock(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel

    await ctx.message.delete()
    ActionLog.create(
        moderator=f"{str(ctx.author)} ({ctx.author.id})",
        action="lock",
        comments=f"Locked {str(channel)}",
    )

    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False

    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

    embed = discord.Embed(
        description=f"Canal `{channel}` verouillé", color=discord.Color.red()
    )
    await ctx.author.send(embed=embed)
    await ctx.send("Canal verrouillé.")


@modobot_client.command(brief="Déverrouille un channel")
async def unlock(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel

    await ctx.message.delete()
    ActionLog.create(
        moderator=f"{str(ctx.author)} ({ctx.author.id})",
        action="unlock",
        comments=f"Unlocked {str(channel)}",
    )

    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True

    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    embed = discord.Embed(
        description=f"Canal `{channel}` déverouillé", color=discord.Color.green()
    )
    await ctx.author.send(embed=embed)
