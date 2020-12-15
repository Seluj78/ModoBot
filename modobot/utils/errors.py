from discord.ext import commands
import logging

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


class UnauthorizedError(commands.BadArgument):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


@modobot_client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await send_error_embed(
            ctx,
            "Missing required arguments",
            "Please pass all required arguments (try `*help`)",
        )
    elif isinstance(error, commands.MissingPermissions):
        await send_error_embed(
            ctx,
            "Incorrect permissions",
            "Contact a higher staff to get the permissions",
        )
    elif isinstance(error, commands.CommandNotFound):
        await send_error_embed(ctx, "Unknown command", "Check `*help`")
    elif isinstance(error, commands.MemberNotFound):
        await send_error_embed(ctx, str(error), "Check the passed member")
    elif isinstance(error, UserAlreadyBannedError):
        await send_error_embed(ctx, str(error), "Someone was first.")
    elif isinstance(error, UnauthorizedError):
        await send_error_embed(ctx, str(error), "You don't have the permissions.")
    elif isinstance(error, commands.CheckFailure):
        logging.error(f"Check failed: {error}")
    else:
        logging.error(f"Unknow error {error}")
        await send_error_embed(ctx, f"Unknow error: {error}", "Try again")
