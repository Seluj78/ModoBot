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
    if ctx.command.name == "ban" and not roleperms.can_ban:
        await ctx.message.delete()
        await ctx.author.send(f"You're not allowed to use `{ctx.command.name}`")
        raise UnauthorizedError(f"You're not allowed to use `{ctx.command.name}`")
    elif ctx.command.name == "unban" and not roleperms.can_unban:
        await ctx.message.delete()
        await ctx.author.send(f"You're not allowed to use `{ctx.command.name}`")
        raise UnauthorizedError(f"You're not allowed to use `{ctx.command.name}`")
    elif ctx.command.name == "warn" and not roleperms.can_warn:
        await ctx.message.delete()
        await ctx.author.send(f"You're not allowed to use `{ctx.command.name}`")
        raise UnauthorizedError(f"You're not allowed to use `{ctx.command.name}`")
    elif ctx.command.name == "note" and not roleperms.can_note:
        await ctx.message.delete()
        await ctx.author.send(f"You're not allowed to use `{ctx.command.name}`")
        raise UnauthorizedError(f"You're not allowed to use `{ctx.command.name}`")
    elif ctx.command.name == "search" and not roleperms.search:
        await ctx.message.delete()
        await ctx.author.send(f"You're not allowed to use `{ctx.command.name}`")
        raise UnauthorizedError(f"You're not allowed to use `{ctx.command.name}`")
    elif ctx.command.name == "clear" and not roleperms.can_clear:
        await ctx.message.delete()
        await ctx.author.send(f"You're not allowed to use `{ctx.command.name}`")
        raise UnauthorizedError(f"You're not allowed to use `{ctx.command.name}`")
    else:
        return True


@modobot_client.check
async def channel_check(ctx):
    allowed_channels = ["commandes"]
    if ctx.message.channel.name not in allowed_channels:
        await ctx.message.delete()
        await ctx.author.send(
            f"The command `{ctx.command.name}` cannot be used in `{ctx.message.channel.name}`"
        )
        raise UnauthorizedError("Cannot use this command in this channel")
    else:
        return True
