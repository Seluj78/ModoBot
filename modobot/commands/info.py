import discord

from modobot import modobot_client
from modobot.models.actionlog import ActionLog
from modobot.utils.france_datetime import datetime_now_france


@modobot_client.command(brief="Informations sur l'utilisateur")
async def info(ctx, member: discord.Member):
    await ctx.message.delete()
    ActionLog.create(
        moderator=f"{str(ctx.author)} ({ctx.author.id})",
        user=f"{str(member)} ({member.id})",
        action="info",
    )

    top_role = member.top_role
    user_joined = member.joined_at
    user_display_name = member.display_name
    user_id = member.id
    user_discordname = str(member)

    embed = discord.Embed(
        title=f"Informations sur {user_display_name} :+1:",
        description=f"`{user_discordname}` (`{user_id}`)",
    )
    embed.add_field(
        name="Status de l'utilisateur",
        value=f"Rejoins le {user_joined}\nGrade le plus haut : {top_role}",
    )
    embed.set_footer(text=f"Action effectuée le {datetime_now_france()}")
    await ctx.channel.send(embed=embed)
