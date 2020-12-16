import discord

from modobot import modobot_client
from modobot.models.actionlog import ActionLog
from modobot.models.userban import UserBan
from modobot.utils.errors import UserAlreadyBannedError
from modobot.utils.errors import UserNotBannedError
from modobot.utils.france_datetime import datetime_now_france


@modobot_client.command(brief="Ban un membre avec la raison donnée")
async def ban(ctx, member: discord.Member, *, reason: str):
    await ctx.message.delete()

    if not member or member == ctx.message.author:
        embed = discord.Embed(
            description="Vous ne pouvez pas vous ban vous-même. :eyes:",
            color=discord.Color.dark_orange(),
        )
        await ctx.author.send(embed=embed)
        return
    if UserBan.get_or_none(banned_id=member.id, is_unbanned=False):
        raise UserAlreadyBannedError(f"L'utilisateur {str(member)} est déjà banni.")

    embed = discord.Embed(
        description=f"Vous avez été banni de `{ctx.guild.name}`.",
        color=discord.Color.red(),
    )
    embed.add_field(name="Raison", value=reason)
    await member.send(embed=embed)

    await member.ban(reason=reason)
    UserBan.create(banned_id=member.id, moderator_id=ctx.author.id, reason=reason)
    ActionLog.create(
        moderator_id=ctx.author.id, user_id=member.id, action="ban", comments=reason
    )

    embed = discord.Embed(
        description=f"`{str(member)}` (`{member.id}`) à été banni.",
        color=discord.Color.red(),
    )
    embed.add_field(name="Raison", value=f"`{reason}`.")
    embed.set_footer(
        text=f"Depuis la commande `{ctx.command.name}` envoyée par {str(ctx.author.name)} dans #{ctx.channel.name}"
    )
    await ctx.channel.send(embed=embed)


@modobot_client.command(brief="Débanne un utilisateur")
async def unban(ctx, *, member_id: str):
    await ctx.message.delete()

    banned_user = UserBan.get_or_none(banned_id=member_id, is_unbanned=False)
    if not banned_user:
        raise UserNotBannedError(f"L'utilisateur {member_id} n'est plus banni.")

    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        if str(ban_entry.user.id) == str(member_id):
            await ctx.guild.unban(ban_entry.user)
            banned_user.is_unbanned = True
            banned_user.dt_unbanned = datetime_now_france()
            banned_user.save()
            ActionLog.create(
                moderator_id=ctx.author.id, user_id=member_id, action="unban"
            )
            embed = discord.Embed(
                description=f"`{member_id}` à été débanni.",
                color=discord.Color.dark_gold(),
            )
            embed.set_footer(
                text=f"Depuis la commande `{ctx.command.name}` "
                f"envoyée par {str(ctx.author.name)} dans #{ctx.channel.name}"
            )
            await ctx.channel.send(embed=embed)
            return
    raise UserNotBannedError(f"L'utilisateur {member_id} n'est pas banni.")
