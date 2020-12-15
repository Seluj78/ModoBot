import os
import discord
import logging
from discord.ext import commands

from dotenv import load_dotenv
from modobot.utils.logging import setup_logging
from modobot.models.userban import UserBan

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

client = commands.Bot(command_prefix='*')


async def send_error_embed(ctx, message, solution):
    embed = discord.Embed(title="Modobot", description="An error has occured", color=discord.Color.red())
    
    embed.add_field(name="Error Message", value=message, inline=True)
    embed.add_field(name="Possible solution", value=solution, inline=False)
    
    await ctx.send(embed=embed)


class UserAlreadyBannedError(commands.BadArgument):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class UserNotBannedError(commands.BadArgument):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


@client.command()
async def ban(ctx, member: discord.Member, *, reason: str):
    
    if UserBan.get_or_none(banned_id=member.id):
        raise UserAlreadyBannedError(f"User {str(member)} is already banned")

    embed = discord.Embed(title="Modobot notification", description=f"You were banned from {ctx.guild.name}", color=discord.Color.red())
    embed.add_field(name="Reason", value=reason, inline=True)
    await member.send(embed=embed)

    await member.ban(reason=reason)
    await ctx.message.delete()
    await ctx.send(f"{ctx.author.id} banned {member.id} for {reason}")
    UserBan.create(
        banned_id=member.id,
        moderator_id=ctx.author.id,
        reason=reason
    ).save()


@client.command()
async def unban(ctx, *, member_id: str):
    banned_user = UserBan.get_or_none(banned_id=member_id)
    if not banned_user:
        raise UserNotBannedError(f"User {member_id} is not banned.")

    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        if str(ban_entry.user.id) == str(member_id):
            await ctx.guild.unban(ban_entry.user)
            banned_user.delete_instance()
            await ctx.message.delete()
            await ctx.send(f"{ctx.author.id} unbanned {member_id}")
            return
    raise UserNotBannedError(f"User {member_id} is not banned.")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await send_error_embed(ctx, 'Missing required arguments', "Please pass all required arguments (try `*help`)")
    elif isinstance(error, commands.MissingPermissions):
        await send_error_embed(ctx, "Incorrect permissions", "Contact a higher staff to get the permissions")
    elif isinstance(error, commands.CommandNotFound):
        await send_error_embed(ctx, "Unknown command", "Check `*help`")
    elif isinstance(error, commands.MemberNotFound):
        await send_error_embed(ctx, str(error), "Check the passed member")
    elif isinstance(error, UserAlreadyBannedError):
        await send_error_embed(ctx, str(error), "Someone was first.")
    else:
        logging.error(f"Unknow error {error}")
        await send_error_embed(ctx, f"Unknow error: {error}", "Try again")


@client.event
async def on_ready():
    logging.info('We have logged in as {0.user}'.format(client))


if __name__ == '__main__':
    setup_logging()
    logging.getLogger("discord").setLevel(logging.WARNING)
    client.run(BOT_TOKEN)
