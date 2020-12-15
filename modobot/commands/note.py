import discord

from modobot import modobot_client
from modobot.models.usernote import UserNote


@modobot_client.command(brief="Adds a note on user only visible to moderators")
async def note(ctx, member: discord.Member, *, reason: str):

    if not member or member == ctx.message.author:
        await ctx.message.delete()
        await ctx.message.author.send("You cannot note yourself")
        return

    UserNote.create(
        notted_id=member.id, moderator_id=ctx.author.id, reason=reason
    ).save()
    await ctx.message.delete()
    await ctx.send(f"{ctx.author.id} added note on {member.id}: {reason}")
