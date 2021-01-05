import discord
from discord.ext.commands import Context

from modobot import modobot_client
from modobot.models.actionlog import ActionLog
from modobot.models.guildsettings import GuildSettings
from modobot.models.role import Role
from modobot.models.rolecategory import RoleCategory
from modobot.utils.converters import RoleCategoryConverter
from modobot.utils.errors import RoleAlreadyInCat
from modobot.utils.errors import RoleAlreadyInSameCat
from modobot.utils.france_datetime import clean_format
from modobot.utils.france_datetime import datetime_now_france


# TODO: Only users with admin role can do it
# TODO: add logging
# TODO: add action logs


@modobot_client.command(
    brief="Crée une catégorie de rôle (0 pour la plus basse, -1 pour la plus haute)"
)
async def addcat(ctx: Context, category_name: str, position: int):
    guildsettings = GuildSettings.get(GuildSettings.guild_id == ctx.guild.id)

    if position == -1:
        position = (
            RoleCategory.select().where(RoleCategory.guild == guildsettings).count()
        )
    else:
        for rolecat in RoleCategory.select().where(
            (RoleCategory.guild == guildsettings) & (RoleCategory.position >= position)
        ):
            rolecat.position += 1
            rolecat.save()

    RoleCategory.create(name=category_name, position=position, guild=guildsettings)
    ActionLog.create(
        moderator_name=str(ctx.author.name),
        moderator_id=ctx.author.id,
        action="addcat",
        comments=f"Added category {category_name} in position {position}",
        guild=guildsettings,
    )
    embed = discord.Embed(
        description=f":white_check_mark: Catégorie {category_name} créée en position {position}",
        color=discord.Color.green(),
    )
    embed.set_footer(text=f"Action effectuée le {clean_format(datetime_now_france())}")
    await ctx.channel.send(embed=embed)


@modobot_client.command(brief="Ajoute un rôle dans une catégorie")
async def addrole(ctx: Context, role: discord.Role, rolecat: RoleCategoryConverter):
    guildsettings = GuildSettings.get(GuildSettings.guild_id == ctx.guild.id)

    if Role.get_or_none(
        (Role.guild == guildsettings)
        & (Role.role_name == role.name)
        & (Role.category == rolecat)
    ):
        raise RoleAlreadyInSameCat("Role already in this category")
    if Role.get_or_none((Role.guild == guildsettings) & (Role.role_name == role.name)):
        raise RoleAlreadyInCat("Role already in a category")

    Role.create(
        role_id=role.id, role_name=role.name, guild=guildsettings, category=rolecat
    )
    embed = discord.Embed(
        description=f":white_check_mark: Role <@&{role.id}> ajouté à la catégorie `{rolecat.name}`",
        color=discord.Color.green(),
    )
    embed.set_footer(text=f"Action effectuée le {clean_format(datetime_now_france())}")

    await ctx.channel.send(embed=embed)


@modobot_client.command(brief="Liste les catégories et leurs rôles correspondants")
async def listcats(ctx: Context):
    guildsettings = GuildSettings.get(GuildSettings.guild_id == ctx.guild.id)
    embed = discord.Embed(
        title="Liste des catégories de rôles", color=discord.Color.orange()
    )

    rolecat_list = RoleCategory.select().where(RoleCategory.guild == guildsettings)

    sorted_list = sorted(rolecat_list, key=lambda i: i.position)

    for rolecat in sorted_list:
        role_list = ""
        for role in rolecat.roles:
            role_list += f"<@&{role.role_id}>\n"
        embed.add_field(
            name=f"{rolecat.name}",
            value=role_list if role_list != "" else "Pas de rôle dans cette catégorie",
            inline=False,
        )
    embed.set_footer(text=f"Action effectuée le {clean_format(datetime_now_france())}")
    await ctx.channel.send(embed=embed)


@modobot_client.command(brief="Supprime un rôle dans une catégorie")
async def delrole(ctx: Context, role: discord.Role):
    guildsettings = GuildSettings.get(GuildSettings.guild_id == ctx.guild.id)
    role = Role.get_or_none(
        (Role.guild == guildsettings) & (Role.role_name == role.name)
    )
    embed = discord.Embed(
        description=f":x: Role <@&{role.role_id}> été supprimé de la catégorie `{role.category.name}`",
        color=discord.Color.red(),
    )
    role.delete_instance()
    embed.set_footer(text=f"Action effectuée le {clean_format(datetime_now_france())}")

    await ctx.channel.send(embed=embed)


@modobot_client.command(brief="Supprime une catégorie de rôles")
async def delcat(ctx: Context, rolecat: RoleCategoryConverter):
    embed = discord.Embed(
        title=f":x: Catégorie `{rolecat.name}` supprimée", color=discord.Color.orange()
    )

    text = ""
    for role in rolecat.roles:
        text += f"<@&{role.role_id}>"
        role.delete_instance()

    embed.add_field(name="Rôle(s) supprimé(s)", value=text)

    rolecat.delete_instance()
    await ctx.channel.send(embed=embed)
