from modobot import modobot_client


@modobot_client.command(brief="Clears X messages from current channel")
async def clear(ctx, clear_size: int):
    await ctx.channel.purge(limit=clear_size)
