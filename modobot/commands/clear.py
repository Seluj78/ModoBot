import logging

from modobot import modobot_client
from modobot.models.actionlog import ActionLog
from modobot.models.guildsettings import GuildSettings
from modobot.utils.archive import send_archive


@modobot_client.command(brief="Supprime X messages dans le canal actuel")
async def clear(ctx, clear_size: int):
    logging.debug("Deleting source message")
    await ctx.message.delete()

    logging.debug(f"Clearing {clear_size} messages in {ctx.channel.name}")
    await ctx.channel.purge(limit=clear_size)
    guildsettings = GuildSettings.get(GuildSettings.guild_id == ctx.guild.id)

    logging.debug("Creating action log for clear")
    actionlog = ActionLog.create(
        moderator_name=str(ctx.author),
        moderator_id=ctx.author.id,
        action="clear",
        comments=f"Cleared {clear_size} in {ctx.channel.id}",
        guild=guildsettings,
    )
    await send_archive(actionlog)
