from modobot import modobot_client
from modobot.models.actionlog import ActionLog


@modobot_client.command(brief="Clears X messages from current channel")
async def clear(ctx, clear_size: int):
    await ctx.channel.purge(limit=clear_size)
    ActionLog.create(
        moderator_id=ctx.author.id, action="clear", comments=f"Cleared {clear_size}"
    )
