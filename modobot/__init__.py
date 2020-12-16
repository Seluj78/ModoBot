import logging
import os

import peewee
from discord.ext import commands
from dotenv import load_dotenv
from peewee import IntegrityError
from pretty_help import PrettyHelp

from modobot.utils.logging import setup_logging

ROOT = os.path.join(os.path.dirname(__file__), "..")  # refers to application_top
dotenv_path = os.path.join(ROOT, ".env")
load_dotenv(dotenv_path)

REQUIRED_ENV_VARS = [
    "DB_HOST",
    "DB_PORT",
    "DB_USER",
    "DB_PASSWORD",
    "DB_NAME",
    "BOT_TOKEN",
    "SERVER_NAME",
]

for item in REQUIRED_ENV_VARS:
    if item not in os.environ:
        raise EnvironmentError(
            f"{item} is not set in the server's environment or .env file. It is required."
        )

from modobot.static import (
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_PORT,
    DB_HOST,
    SERVER_NAME,
)  # noqa

setup_logging()

modobot_client = commands.Bot(command_prefix="?", help_command=PrettyHelp())


modo_db = peewee.MySQLDatabase(
    database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
)


@modobot_client.event
async def on_ready():
    logging.info("We have logged in as {0.user}".format(modobot_client))
    from modobot.models.roleperms import RolePerms

    logging.info("Setting all roles")
    for guild in modobot_client.guilds:
        if guild.name == SERVER_NAME:
            for role in guild.roles:
                if role.name == "@everyone":
                    continue
                try:
                    RolePerms.create(name=role.name)
                except IntegrityError:
                    pass
    logging.info("All roles created")


from modobot.models.userban import UserBan
from modobot.models.userwarn import UserWarn
from modobot.models.usernote import UserNote
from modobot.models.actionlog import ActionLog
from modobot.models.roleperms import RolePerms

if not UserBan.table_exists():
    UserBan.create_table()
if not UserWarn.table_exists():
    UserWarn.create_table()
if not UserNote.table_exists():
    UserNote.create_table()
if not ActionLog.table_exists():
    ActionLog.create_table()
if not RolePerms.table_exists():
    RolePerms.create_table()


import modobot.utils.checks  # noqa
import modobot.commands.ban  # noqa
import modobot.commands.clear  # noqa
import modobot.commands.warn  # noqa
import modobot.commands.note  # noqa
import modobot.commands.search  # noqa
import modobot.commands.lock  # noqa
import modobot.commands.info  # noqa
