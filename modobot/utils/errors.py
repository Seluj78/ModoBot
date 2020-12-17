import logging

import discord
from discord.ext import commands

from modobot import modobot_client
from modobot.utils.embeds import send_error_embed


class UserAlreadyBannedError(commands.BadArgument):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class UserNotBannedError(commands.BadArgument):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class IncorrectTimeError(commands.BadArgument):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class UnauthorizedError(commands.BadArgument):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class PunishSelfError(commands.BadArgument):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class PunishBotError(commands.BadArgument):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


@modobot_client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(description=":x: Argument(s) requis manquant(s)")
        await ctx.channel.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        await send_error_embed(
            ctx, "Permissions incorrectes.", "Contactez un staff supérieur."
        )
    elif isinstance(error, commands.CommandNotFound):
        await send_error_embed(ctx, "Commande inconnue", "")
    elif isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(description=f":grey_question: {str(error)}")
        await ctx.channel.send(embed=embed)
    elif isinstance(error, PunishBotError):
        embed = discord.Embed(description=f":x: {str(error)}")
        await ctx.channel.send(embed=embed)
    elif isinstance(error, UserAlreadyBannedError):
        await send_error_embed(ctx, str(error), "Cet utilisateur est déjà banni")
    elif isinstance(error, UserNotBannedError):
        embed = discord.Embed(description=f":x: {str(error)}")
        await ctx.channel.send(embed=embed)
    elif isinstance(error, UnauthorizedError):
        embed = discord.Embed(
            description=f":x: Vous n'êtes pas autorisé à utiliser {ctx.command.name}."
        )
        embed.set_footer(
            text="Contactez un administrateur si vous pensez que c'est une erreur."
        )
        await ctx.channel.send(embed=embed)
    elif isinstance(error, commands.CheckFailure):
        logging.error(f"Check failed: {error}")
    elif isinstance(error, IncorrectTimeError):
        await send_error_embed(ctx, str(error), "Format incorrect")
    elif isinstance(error, PunishSelfError):
        await send_error_embed(ctx, str(error), "Nope")
    else:
        logging.error(f"Unknow error {error}")
        await send_error_embed(ctx, f"Erreur inconnue: {error}", "Essayez a nouveau")


@modobot_client.after_invoke
async def after_invoke(ctx):
    pass
