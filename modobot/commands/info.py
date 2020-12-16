import discord

from modobot import modobot_client
from modobot.models.actionlog import ActionLog


@modobot_client.command(brief="Informations sur l'utilisateur")
async def info(ctx, member: discord.Member):

    ActionLog.create(moderator_id=ctx.author.id, user_id=member.id, action="info")

    top_role = member.top_role
    user_joined = member.joined_at
    user_display_name = member.display_name
    user_id = member.id
    user_discordname = str(member)

    embed = discord.Embed(
        title=f"Informations sur {user_display_name}",
        description=f"`{user_discordname}` (`{user_id}`)",
    )
    embed.add_field(
        name="Status de l'utilisateur",
        value=f"Rejoins le {user_joined}\nGrade le plus haut : {top_role}",
    )
    await ctx.channel.send(embed=embed)
