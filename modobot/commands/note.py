import discord

from modobot import modobot_client
from modobot.models.actionlog import ActionLog
from modobot.models.usernote import UserNote


@modobot_client.command(brief="Adds a note on user only visible to moderators")
async def note(ctx, member: discord.Member, *, reason: str):
    await ctx.message.delete()
    if not member or member == ctx.message.author:
        embed = discord.Embed(
            description="You cannot note yourself.", color=discord.Color.dark_orange()
        )
        await ctx.author.send(embed=embed)
        return

    UserNote.create(notted_id=member.id, moderator_id=ctx.author.id, reason=reason)

    embed = discord.Embed(
        description=f"Note added on `{str(member)}` (`{member.id}`).",
        color=discord.Color.blurple(),
    )
    embed.add_field(name="Note", value=f"`{reason}`.")
    embed.set_footer(
        text=f"From command `{ctx.command.name}` sent by {str(ctx.author.name)} in #{ctx.channel.name}"
    )
    await ctx.channel.send(embed=embed)

    ActionLog.create(
        moderator_id=ctx.author.id, user_id=member.id, action="note", comments=reason
    )
