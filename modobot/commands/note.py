import logging

import discord

from modobot import modobot_client
from modobot.models.actionlog import ActionLog
from modobot.models.usernote import UserNote
from modobot.utils.archive import send_archive
from modobot.utils.france_datetime import clean_format
from modobot.utils.france_datetime import datetime_now_france


@modobot_client.command(brief="Ajoute une note seulement visible par les modérateurs")
async def note(ctx, member: discord.Member, *, reason: str):
    logging.debug("Deleting source message")
    await ctx.message.delete()

    logging.debug("Creating note in database")
    UserNote.create(noted_id=member.id, moderator_id=ctx.author.id, reason=reason)

    logging.debug("Creating action log for nnote")
    new_log = ActionLog.create(
        moderator_name=str(ctx.author),
        moderator_id=ctx.author.id,
        user_name=str(member),
        user_id=member.id,
        action="note",
        comments=reason,
    )

    logging.debug("Creating embed")
    embed = discord.Embed(
        description=f":notepad_spiral: Note ajoutée sur `{str(member)}` (`{member.id}`).",
        color=discord.Color.blurple(),
    )
    embed.add_field(name="Note", value=reason)
    embed.set_footer(text=f"Action effectuée le {clean_format(datetime_now_france())}")
    logging.debug("Sending embed")
    await ctx.channel.send(embed=embed)
    logging.debug("Sending note archive")
    await send_archive(actionlog=new_log)
