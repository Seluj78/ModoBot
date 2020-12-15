import discord

from modobot import modobot_client
from modobot.models.actionlog import ActionLog
from modobot.models.userban import UserBan
from modobot.models.usernote import UserNote
from modobot.models.userwarn import UserWarn


@modobot_client.command(brief="Recherche dans la DB sur un utilisateur")
async def search(ctx, member: discord.Member):
    ActionLog.create(moderator_id=ctx.author.id, action="search", comments=member.id)
    notes = UserNote.select().where(UserNote.noted_id == member.id)
    warns = UserWarn.select().where(UserWarn.warned_id == member.id)
    bans = UserBan.select().where(UserBan.banned_id == member.id)
    embed = discord.Embed(color=discord.Color.blue())
    if notes:
        msg = """"""
        for note in notes:
            msg += f"{note.moderator_id} à noté `{note.reason}` le {note.dt_noted}\n--------\n"
        embed.add_field(name="Notes", value=msg, inline=False)
    if warns:
        msg = """"""
        for warn in warns:
            msg += f"{warn.moderator_id} à averti `{warn.reason}` le {warn.dt_warned}\n--------\n"
        embed.add_field(name="Warns", value=msg, inline=False)
    if bans:
        msg = """"""
        for ban in bans:
            msg += f"{ban.moderator_id} à banni avec comme raison `{ban.reason}` le {ban.dt_banned}"
            if ban.is_unbanned:
                msg += f" (débanni le {ban.dt_unbanned})\n--------\n"
            else:
                msg += "\n"
        embed.add_field(name="Bans", value=msg, inline=False)
    embed.set_footer(text=f"Recherche sur l'utilisateur {str(member)} ({member.id})")

    await ctx.channel.send(embed=embed)
