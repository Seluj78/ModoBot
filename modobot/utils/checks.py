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
        raise UnauthorizedError("Vous n'êtes pas authorisé à utiliser cette commande.")
    if not roleperms.is_staff:
        await ctx.message.delete()
        raise UnauthorizedError("Vous n'êtes pas authorisé à utiliser cette commande.")
    if ctx.command.name == "help":
        return True
    if not getattr(roleperms, "can_" + ctx.command.name, False):
        if not roleperms.silence_notif:
            await ctx.message.delete()
            await ctx.author.send(
                f"Vous n'êtes pas autorisé à utiliser `{ctx.command.name}`"
            )
        raise UnauthorizedError(
            f"Vous n'êtes pas autorisé à utiliser `{ctx.command.name}`"
        )
    else:
        return True


@modobot_client.check
async def channel_check(ctx):
    allowed_channels = ["commandes"]
    if ctx.message.channel.name not in allowed_channels:
        await ctx.message.delete()
        await ctx.author.send(
            f"La commande `{ctx.command.name}` ne peut pas être utilisée dans `{ctx.message.channel.name}`"
        )
        raise UnauthorizedError("Impossible d'utiliser cette commande dans ce canal")
    else:
        return True
