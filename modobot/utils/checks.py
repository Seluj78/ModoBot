from modobot import modobot_client


@modobot_client.check
async def permissions_check(ctx):
    allowed_roles = [788149895726628875]
    role_ids = [role.id for role in ctx.author.roles]
    for role in role_ids:
        if role in allowed_roles:
            return True
    await ctx.message.delete()
    await ctx.author.send(f"You are not authorized to use `{ctx.command.name}`")
    return False


@modobot_client.check
async def channel_check(ctx):
    allowed_channels = ["commandes"]
    if ctx.message.channel.name not in allowed_channels:
        await ctx.message.delete()
        await ctx.author.send(f"The command `{ctx.command.name}` cannot be used in `{ctx.message.channel.name}`")
        return False
    else:
        return True

