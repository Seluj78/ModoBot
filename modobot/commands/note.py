import discord

from modobot import modobot_client
from modobot.models.actionlog import ActionLog
from modobot.models.usernote import UserNote
from modobot.utils.france_datetime import datetime_now_france


@modobot_client.command(brief="Ajoute une note seulement visible par les modérateurs")
async def note(ctx, member: discord.Member, *, reason: str):
    await ctx.message.delete()

    UserNote.create(noted_id=member.id, moderator_id=ctx.author.id, reason=reason)
    ActionLog.create(
        moderator=f"{str(ctx.author)} ({ctx.author.id})",
        user=f"{str(member)} ({member.id})",
        action="note",
        comments=reason,
    )

    embed = discord.Embed(
        description=f":notepad_spiral: Note ajoutée sur `{str(member)}` (`{member.id}`).",
        color=discord.Color.blurple(),
    )
    embed.add_field(name="Note", value=reason)
    embed.set_footer(text=f"Action effectuée le {datetime_now_france()}")
    await ctx.channel.send(embed=embed)
