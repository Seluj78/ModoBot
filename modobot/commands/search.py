import discord
from modobot import modobot_client
from modobot.models.actionlog import ActionLog
from modobot.models.userban import UserBan
from modobot.models.usernote import UserNote
from modobot.models.userwarn import UserWarn


@modobot_client.command(brief="Search for user in all DBs")
async def search(ctx, member: discord.Member):
    ActionLog.create(
        moderator_id=ctx.author.id, action="search", comments=member.id
    )
    notes = UserNote.select().where(UserNote.noted_id == member.id)
    warns = UserWarn.select().where(UserWarn.warned_id == member.id)
    bans = UserBan.select().where(UserBan.banned_id == member.id)
    embed = discord.Embed(color=discord.Color.blue())
    if notes:
        msg = """"""
        for note in notes:
            msg += f"{note.moderator_id} noted `{note.reason}` on {note.dt_noted}\n--------\n"
        embed.add_field(name="Notes", value=msg, inline=False)
    if warns:
        msg = """"""
        for warn in warns:
            msg += f"{warn.moderator_id} warned `{warn.reason}` on {warn.dt_warned}\n--------\n"
        embed.add_field(name="Warns", value=msg, inline=False)
    if bans:
        msg = """"""
        for ban in bans:
            msg += f"{ban.moderator_id} noted `{ban.reason}` on {ban.dt_banned}"
            if ban.is_unbanned:
                msg += f" (Unbanned on {ban.dt_unbanned})\n--------\n"
            else:
                msg += "\n"
        embed.add_field(name="Bans", value=msg, inline=False)
    embed.set_footer(text=f"Search on user {str(member)} ({member.id})")

    await ctx.channel.send(embed=embed)
