import discord

from modobot import modobot_client
from modobot.models.actionlog import ActionLog
from modobot.utils.france_datetime import datetime_now_france


@modobot_client.command(brief="Supprime X messages dans le canal actuel")
async def clear(ctx, clear_size: int):
    await ctx.message.delete()

    await ctx.channel.purge(limit=clear_size)

    ActionLog.create(
        moderator=f"{str(ctx.author)} ({ctx.author.id})",
        action="clear",
        comments=f"Cleared {clear_size}",
    )

    embed = discord.Embed(
        description=f"**{clear_size} messages** on été supprimés dans `{ctx.channel.name}`",
        color=discord.Color.gold(),
    )
    embed.set_footer(text=f"Action effectuée le {datetime_now_france()}")
    await ctx.channel.send(embed=embed)
