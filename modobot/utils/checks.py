import contextlib
import logging

import discord

from modobot import modobot_client
from modobot.models.roleperms import RolePerms
from modobot.models.unautorized_report import UnauthorizedReport
from modobot.static import COMMAND_CHANNEL_ID
from modobot.utils.errors import UnauthorizedError


@modobot_client.check
async def permissions_check(ctx):
    logging.debug(f"Checking permissions for {str(ctx.author)} for {ctx.command.name}")
    role_names = [role.name for role in ctx.author.roles]
    for role in role_names:
        roleperms = RolePerms.get_or_none(name=role)
        if roleperms:
            logging.debug(f"Found roleperm {roleperms.id}")
            break
    if not roleperms:
        logging.warning("No roleperm found, sending error")
        await ctx.message.delete()
        UnauthorizedReport.create(
            moderator_name=str(ctx.author),
            moderator_id=ctx.author.id,
            command=ctx.command,
            type="permissions",
        )
        raise UnauthorizedError("Vous n'êtes pas authorisé à utiliser cette commande.")
    if not roleperms.is_staff:
        logging.warning("User is not staff, sending error")
        await ctx.message.delete()
        UnauthorizedReport.create(
            moderator_name=str(ctx.author),
            moderator_id=ctx.author.id,
            command=ctx.command,
            type="permissions",
        )
        raise UnauthorizedError("Vous n'êtes pas authorisé à utiliser cette commande.")
    if ctx.command.name == "help":
        logging.debug("Command is help, ignoring permissions check")
        return True
    if not getattr(roleperms, "can_" + ctx.command.name, False):
        logging.debug(
            f"User {str(ctx.author)} doesn't have the permission to perform {ctx.command.name}"
        )
        if not roleperms.silence_notif:
            await ctx.message.delete()
            UnauthorizedReport.create(
                moderator_name=str(ctx.author),
                moderator_id=ctx.author.id,
                command=ctx.command,
                type="permissions",
            )
            with contextlib.suppress(discord.Forbidden):
                await ctx.author.send(
                    f"Vous n'êtes pas autorisé à utiliser `{ctx.command.name}`"
                )
        UnauthorizedReport.create(
            moderator_name=str(ctx.author),
            moderator_id=ctx.author.id,
            command=ctx.command,
            type="permissions",
        )
        raise UnauthorizedError(
            f"Vous n'êtes pas autorisé à utiliser `{ctx.command.name}`"
        )
    else:
        return True


@modobot_client.check
async def channel_check(ctx):
    logging.debug(
        f"Checking if command {ctx.command.name} can be used in {ctx.channel.name}"
    )
    if ctx.command.name == "clear":
        logging.debug("Command is 'clear', allowing")
        return True
    if ctx.message.channel.id != int(COMMAND_CHANNEL_ID):
        logging.debug(
            f"User {str(ctx.author)} sent command {ctx.command.name} in channel {ctx.channel.name} which is not allowed"
        )
        await ctx.message.delete()
        with contextlib.suppress(discord.Forbidden):
            await ctx.author.send(
                f"La commande `{ctx.command.name}` ne peut pas être utilisée dans `{ctx.message.channel.name}`"
            )
        UnauthorizedReport.create(
            moderator_name=str(ctx.author),
            moderator_id=ctx.author.id,
            command=ctx.command,
            type="channel",
        )
        raise UnauthorizedError("Impossible d'utiliser cette commande dans ce canal")
    else:
        return True
