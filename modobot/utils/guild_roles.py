import logging

from discord import Guild

from modobot.models.roleperms import RolePerms


async def set_guild_roles(guild: Guild, guildsettings):
    for role in guild.roles:
        RolePerms.create(role_name=role.name, role_id=role.id, guild=guildsettings)
        logging.debug(f"Added role {role.name} in guild {guild.id}")
