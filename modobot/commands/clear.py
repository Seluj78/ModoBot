from modobot import modobot_client


@modobot_client.command()
async def clear(ctx, clear_size: int):
    await ctx.channel.purge(limit=clear_size)
