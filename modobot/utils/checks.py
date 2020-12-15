from modobot import modobot_client
from modobot.role_matrice import ROLE_MATRIX
import logging


@modobot_client.check
async def permissions_check(ctx):
    role_names = [role.name for role in ctx.author.roles]
    for role in role_names:
        try:
            if ROLE_MATRIX[role][ctx.command.name]:
                return True
        except KeyError:
            logging.debug(f"Ignored role {role}")
            continue
    await ctx.message.delete()
    await ctx.author.send(f"You are not authorized to use `{ctx.command.name}`")
    return False


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
