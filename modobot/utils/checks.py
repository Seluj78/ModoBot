import logging

from discord.ext.commands import Context

from modobot import modobot_client
from modobot.models.guildsettings import GuildSettings
from modobot.models.role import Role
from modobot.models.unautorized_report import UnauthorizedReport
from modobot.utils.errors import UnauthorizedError
from modobot.utils.errors import UnfinishedBotConfigError

# from modobot.static import COMMAND_CHANNEL_ID
# from modobot.utils.errors import UnauthorizedChannelError

# TODO: Add check if guild settings are configured.


@modobot_client.check
async def guild_settings_check(ctx: Context):
    guildsettings = GuildSettings.get(GuildSettings.guild_id == ctx.guild.id)
    if (
        guildsettings.muted_role_id != 0
        and guildsettings.archive_channel_id != 0
        and guildsettings.master_user_id != 0
    ):
        return True
    else:
        raise UnfinishedBotConfigError("La configuration du bot est incomplète")


@modobot_client.check
async def permissions_check(ctx: Context):
    logging.debug(
        f"Checking permissions for {str(ctx.author)} for {ctx.command.name} in {ctx.guild.name}"
    )
    guildsettings = GuildSettings.get(GuildSettings.guild_id == ctx.guild.id)

    if ctx.author.id == guildsettings.master_user_id:
        return True

    role = None
    for r in ctx.author.roles:
        role = Role.get_or_none(role_id=r.id, guild=guildsettings)
        if role:
            logging.debug(f"Found role in db {role.id}")
            break
    if not role:
        logging.warning("No role found, sending error")
        await ctx.message.delete()
        UnauthorizedReport.create(
            moderator_name=str(ctx.author),
            moderator_id=ctx.author.id,
            command=ctx.command,
            type="permissions",
            guild=guildsettings,
        )
        raise UnauthorizedError("Vous n'êtes pas authorisé à utiliser cette commande.")
    if ctx.command.name == "help":
        logging.debug("Command is help, ignoring permissions check")
        return True
    if not getattr(role.category, "can_" + ctx.command.name, False):
        logging.debug(
            f"User {str(ctx.author)} doesn't have the permission to perform {ctx.command.name}"
        )
        await ctx.message.delete()
        UnauthorizedReport.create(
            moderator_name=str(ctx.author),
            moderator_id=ctx.author.id,
            command=ctx.command,
            type="permissions",
            guild=guildsettings,
        )
        UnauthorizedReport.create(
            moderator_name=str(ctx.author),
            moderator_id=ctx.author.id,
            command=ctx.command,
            type="permissions",
            guild=guildsettings,
        )
        raise UnauthorizedError(
            f"Vous n'êtes pas autorisé à utiliser `{ctx.command.name}`"
        )
    else:
        return True


# @modobot_client.check
# async def channel_check(ctx):
#     logging.debug(
#         f"Checking if command {ctx.command.name} can be used in {ctx.channel.name}"
#     )
#     # TODO: Make this a guild setting
#     if ctx.command.name in ["clear", "lock", "unlock"]:
#         logging.debug(
#             f"Command is {ctx.command.name}, allowing to use in {ctx.channel.name}"
#         )
#         return True
#     if ctx.message.channel.id != int(COMMAND_CHANNEL_ID):
#         logging.debug(
#             f"User {str(ctx.author)} sent command {ctx.command.name} "
#             f"in channel {ctx.channel.name} which is not allowed"
#         )
#         await ctx.message.delete()
#         with contextlib.suppress(discord.Forbidden):
#             await ctx.author.send(
#                 f"La commande `{ctx.command.name}` ne peut pas être utilisée dans `{ctx.message.channel.name}`"
#             )
#         guildsettings = GuildSettings.get(GuildSettings.guild_id == ctx.guild.id)
#         UnauthorizedReport.create(
#             moderator_name=str(ctx.author),
#             moderator_id=ctx.author.id,
#             command=ctx.command,
#             type="channel",
#             guild=guildsettings,
#         )
#         raise UnauthorizedChannelError(
#             "Impossible d'utiliser cette commande dans ce canal"
#         )
#     else:
#         return True
