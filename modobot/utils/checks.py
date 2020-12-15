from modobot import modobot_client
from modobot.models.roleperms import RolePerms
from modobot.utils.errors import UnauthorizedError


@modobot_client.check
async def permissions_check(ctx):
    role_names = [role.name for role in ctx.author.roles]
    for role in role_names:
        roleperms = RolePerms.get_or_none(name=role)
        if roleperms:
            break
    if not roleperms:
        await ctx.message.delete()
        raise UnauthorizedError("You're not allowed to use this command")
    if ctx.command.name == "ban":
        return roleperms.can_ban
    elif ctx.command.name == "unban":
        return roleperms.can_unban
    elif ctx.command.name == "warn":
        return roleperms.can_warn
    elif ctx.command.name == "note":
        return roleperms.can_note
    elif ctx.command.name == "search":
        return roleperms.search
    elif ctx.command.name == "clear":
        return roleperms.can_clear


@modobot_client.check
async def channel_check(ctx):
    allowed_channels = ["commandes"]
    if ctx.message.channel.name not in allowed_channels:
        await ctx.message.delete()
        await ctx.author.send(
            f"The command `{ctx.command.name}` cannot be used in `{ctx.message.channel.name}`"
        )
        return False
    else:
        return True
