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


class PunishStaffError(commands.BadArgument):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class AlreadyMuteError(commands.BadArgument):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class NotMutedError(commands.BadArgument):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


@modobot_client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        embed = discord.Embed(description=":x: Argument(s) requis manquant(s)")
        await ctx.channel.send(embed=embed)
    elif isinstance(error, commands.CommandNotFound):
        await ctx.message.delete()
        embed = discord.Embed(description=":x: Commande inconnue")
        await ctx.channel.send(embed=embed)
    elif isinstance(error, commands.MemberNotFound):
        await ctx.message.delete()
        embed = discord.Embed(description=f":grey_question: {str(error)}")
        await ctx.channel.send(embed=embed)
    elif isinstance(error, PunishBotError):
        await ctx.message.delete()
        embed = discord.Embed(description=f":x: {str(error)}")
        await ctx.channel.send(embed=embed)
    elif isinstance(error, NotMutedError):
        embed = discord.Embed(description=f":x: {str(error)}")
        await ctx.channel.send(embed=embed)
    elif isinstance(error, PunishStaffError):
        await ctx.message.delete()
        embed = discord.Embed(description=f":x: {str(error)}")
        await ctx.channel.send(embed=embed)
    elif isinstance(error, AlreadyMuteError):
        embed = discord.Embed(description=f":x: {str(error)}")
        await ctx.channel.send(embed=embed)
    elif isinstance(error, UserAlreadyBannedError):
        await ctx.message.delete()
        embed = discord.Embed(description=":x: Cet utilisateur est déjà banni.")
        await ctx.channel.send(embed=embed)
    elif isinstance(error, UserNotBannedError):
        await ctx.message.delete()
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
        logging.warning(f"Check failed: {error}")
        await send_error_embed(ctx, f"Erreur de check: {error}", "Essayez a nouveau")
    elif isinstance(error, IncorrectTimeError):
        embed = discord.Embed(description=":x: Format incorrect")
        await ctx.channel.send(embed=embed)
    else:
        logging.error(f"Unknow error {error}")
        await send_error_embed(ctx, f"Erreur inconnue: {error}", "Essayez a nouveau")
