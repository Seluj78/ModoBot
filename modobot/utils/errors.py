import logging

import discord
from discord.ext import commands

from modobot import modobot_client
from modobot.utils.embeds import send_error_embed


class RoleAlreadyInSameCat(commands.BadArgument):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class RoleAlreadyInCat(commands.BadArgument):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class RoleCatDoesntExist(commands.BadArgument):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


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


class UnauthorizedChannelError(commands.BadArgument):
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


class UnfinishedBotConfigError(commands.BadArgument):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


error_dict = {
    NotMutedError: {
        "message": ":x: L'utilisateur n'est pas mute.",
        "color": discord.Color.red(),
        "send_to": "channel",
    },
    AlreadyMuteError: {
        "message": ":x: L'utilisateur est déjà mute.",
        "color": discord.Color.red(),
        "send_to": "channel",
    },
    PunishStaffError: {
        "message": ":x: Vous ne pouvez pas punir un autre membre du staff.",
        "color": discord.Color.red(),
        "send_to": "channel",
    },
    PunishBotError: {
        "message": ":x: Pourquoi me faire tant de mal, je ne suis qu'un bot :robot:.",
        "color": discord.Color.red(),
        "send_to": "channel",
    },
    commands.MissingRequiredArgument: {
        "message": ":x: Argument(s) requis manquant(s).",
        "color": discord.Color.red(),
        "send_to": "channel",
    },
    commands.CommandNotFound: {
        "message": ":x: Commande inconnue.",
        "color": discord.Color.red(),
        "send_to": "channel",
    },
    commands.MemberNotFound: {
        "message": ":grey_question: Utilisateur inconnu.",
        "color": discord.Color.red(),
        "send_to": "channel",
    },
    UserAlreadyBannedError: {
        "message": ":x: Cet utilisateur est déjà banni.",
        "color": discord.Color.red(),
        "send_to": "channel",
    },
    UserNotBannedError: {
        "message": ":x: Cet utilisateur n'est pas banni.",
        "color": discord.Color.red(),
        "send_to": "channel",
    },
    IncorrectTimeError: {
        "message": ":x: Format de temps incorrect.",
        "color": discord.Color.red(),
        "send_to": "channel",
    },
    RoleAlreadyInSameCat: {
        "message": ":x: Ce rôle est déjà dans cette catégorie.",
        "color": discord.Color.red(),
        "send_to": "channel",
    },
    RoleAlreadyInCat: {
        "message": ":x: Ce rôle est déjà dans une catégorie.",
        "color": discord.Color.red(),
        "send_to": "channel",
    },
    RoleCatDoesntExist: {
        "message": ":x: La catégorie demandée n'existe pas.",
        "color": discord.Color.red(),
        "send_to": "channel",
    },
    UnfinishedBotConfigError: {
        "message": ":x: La configuration du bot n'est pas fini.",
        "color": discord.Color.red(),
        "send_to": "channel",
    },
}


@modobot_client.event
async def on_command_error(ctx, error):
    data = error_dict.get(type(error))
    if data:
        embed = discord.Embed(description=data["message"], color=data["color"])
        if data["send_to"] == "channel":
            await ctx.channel.send(embed=embed)
        else:
            await ctx.author.send(embed=embed)
    else:
        if isinstance(error, UnauthorizedError):
            embed = discord.Embed(
                description=f":x: Vous n'êtes pas autorisé à utiliser {ctx.command.name}.",
                color=discord.Color.red(),
            )
            embed.set_footer(
                text="Contactez un administrateur si vous pensez que c'est une erreur."
            )
            await ctx.channel.send(embed=embed)
        elif isinstance(error, UnauthorizedChannelError):
            embed = discord.Embed(
                description=f":x: Vous n'êtes pas autorisé à utiliser {ctx.command.name} dans {ctx.channel.name}.",
                color=discord.Color.red(),
            )
            embed.set_footer(
                text="Contactez un administrateur si vous pensez que c'est une erreur."
            )
            await ctx.author.send(embed=embed)
        elif isinstance(error, commands.CheckFailure):
            logging.warning(f"Check failed: {error}")
            await send_error_embed(
                ctx, f"Erreur de check: {error}", "Essayez a nouveau"
            )
        else:
            logging.error(f"Unknow error {error}")
            await send_error_embed(
                ctx, f"Erreur inconnue: {error}", "Essayez a nouveau"
            )
