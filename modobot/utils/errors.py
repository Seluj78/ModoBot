import logging

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


@modobot_client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await send_error_embed(
            ctx,
            "Arguments requis manquants",
            "Merci de passer tous les arguments nécéssaires.",
        )
    elif isinstance(error, commands.MissingPermissions):
        await send_error_embed(
            ctx, "Permissions incorrectes.", "Contactez un staff supérieur."
        )
    elif isinstance(error, commands.CommandNotFound):
        await send_error_embed(ctx, "Commande inconnue", "")
    elif isinstance(error, commands.MemberNotFound):
        await send_error_embed(
            ctx, str(error), "Verifiez l'utilisateur passé en paramettre"
        )
    elif isinstance(error, UserAlreadyBannedError):
        await send_error_embed(ctx, str(error), "Cet utilisateur est déjà banni")
    elif isinstance(error, UnauthorizedError):
        logging.debug(f"Got unauthorized error: {str(error)}")
    elif isinstance(error, commands.CheckFailure):
        logging.error(f"Check failed: {error}")
    elif isinstance(error, IncorrectTimeError):
        await send_error_embed(ctx, str(error), "Format incorrect")
    else:
        logging.error(f"Unknow error {error}")
        await send_error_embed(ctx, f"Erreur inconnue: {error}", "Essayez a nouveau")


@modobot_client.after_invoke
async def after_invoke(ctx):
    pass
