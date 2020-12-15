import discord

from modobot import modobot_client
from modobot.models.actionlog import ActionLog
from modobot.models.usernote import UserNote


@modobot_client.command(brief="Ajoute une note seulement visible par les modérateurs")
async def note(ctx, member: discord.Member, *, reason: str):
    await ctx.message.delete()

    if not member or member == ctx.message.author:
        embed = discord.Embed(
            description="Vous ne pouvez pas vous notez vous même. :eyes:",
            color=discord.Color.dark_orange(),
        )
        await ctx.author.send(embed=embed)
        return

    UserNote.create(notted_id=member.id, moderator_id=ctx.author.id, reason=reason)
    ActionLog.create(
        moderator_id=ctx.author.id, user_id=member.id, action="note", comments=reason
    )

    embed = discord.Embed(
        description=f"Note ajoutée sur `{str(member)}` (`{member.id}`).",
        color=discord.Color.blurple(),
    )
    embed.add_field(name="Note", value=f"`{reason}`.")
    embed.set_footer(
        text=f"Depuis la commande `{ctx.command.name}` envoyée par {str(ctx.author.name)} dans #{ctx.channel.name}"
    )
    await ctx.channel.send(embed=embed)
