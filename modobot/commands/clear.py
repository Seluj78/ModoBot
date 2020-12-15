import discord

from modobot import modobot_client
from modobot.models.actionlog import ActionLog


@modobot_client.command(brief="Clears X messages from current channel")
async def clear(ctx, clear_size: int):
    await ctx.message.delete()

    await ctx.channel.purge(limit=clear_size)

    ActionLog.create(
        moderator_id=ctx.author.id, action="clear", comments=f"Cleared {clear_size}"
    )

    embed = discord.Embed(
        description=f"Successfully cleared `{clear_size}` messages in `{ctx.channel.name}`",
        color=discord.Color.gold(),
    )
    await ctx.author.send(embed=embed)
