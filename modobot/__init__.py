import asyncio
import contextlib
import json
import logging
import os
from datetime import datetime

import discord
import peewee
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from peewee import DoesNotExist
from peewee import IntegrityError
from pretty_help import PrettyHelp

from modobot.utils.france_datetime import datetime_now_france
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
    "FLASK_SECRET_KEY",
    "SERVER_ID",
    "ARCHIVE_CHANNEL_ID",
    "COMMAND_CHANNEL_ID",
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
    FLASK_SECRET_KEY,
    SERVER_ID,
)  # noqa

setup_logging()

application = Flask(__name__)

application.debug = os.getenv("FLASK_DEBUG") in ("true", "1")

application.secret_key = FLASK_SECRET_KEY
application.config.update(FLASK_SECRET_KEY=FLASK_SECRET_KEY)
application.config["FLASK_ADMIN_SWATCH"] = "lux"

# Initializes the login manager used for the admin
login_manager = LoginManager()
login_manager.init_app(application)


# Loads the user when a request is done to a protected page
@login_manager.user_loader
def load_user(uid):
    try:
        return AdminUser.get_by_id(uid)
    except DoesNotExist:
        return None


logging.debug("Creating bot object")
modobot_client = commands.Bot(command_prefix="?", help_command=PrettyHelp())

logging.debug("Connecting to database")
modo_db = peewee.MySQLDatabase(
    database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
)


async def unmute_user_after(usermute, skip=False):
    if not skip:
        logging.debug(
            f"Usermute {usermute.id}: Sleeping {(usermute.dt_unmute - datetime.now()).seconds} seconds."
        )
        await asyncio.sleep((usermute.dt_unmute - datetime.now()).seconds)

    logging.debug("Getting guild from server id")
    guild = modobot_client.get_guild(int(SERVER_ID))

    logging.debug("Finding role Muted")
    for role in guild.roles:
        if role.name == "Muted":
            break
    if not role:
        raise ValueError("Role 'Muted' not found")

    logging.debug("Getting muted member")
    member = await guild.fetch_member(int(usermute.muted_id))
    logging.debug("Removing muted role")
    await member.remove_roles(role)

    logging.debug(f"Getting last mute for member {member.id}")
    last_mute = (
        UserMute.select()
        .where(UserMute.muted_id == member.id)
        .order_by(UserMute.id.desc())
        .get()
    )
    logging.debug("Setting last mute to unmuted")
    last_mute.is_unmuted = True
    last_mute.dt_unmuted = datetime_now_france()
    last_mute.save()

    logging.debug("Restoring roles to user")
    for role_id in json.loads(last_mute.user_roles):
        role = guild.get_role(role_id)
        logging.debug(f"Adding role {role.name}")
        await member.add_roles(role)

    logging.debug("Creating action log for automatic unmute")
    new_log = ActionLog.create(
        moderator_name="automatic",
        moderator_id=0,
        user_name=str(member),
        user_id=member.id,
        action="unmute",
    )

    embed = discord.Embed(
        description=f":raised_hands: Vous avez été unmute de `{guild.name}`.",
        color=discord.Color.green(),
    )
    embed.set_footer(text=f"Action effectuée le {datetime_now_france()}")
    with contextlib.suppress(discord.Forbidden):
        logging.debug("Sending embed to user")
        await member.send(embed=embed)
    from modobot.utils.archive import send_archive

    logging.debug("Sending unmute archive")
    await send_archive(new_log)


@modobot_client.event
async def on_ready():
    logging.info("We have logged in as {0.user}".format(modobot_client))
    from modobot.models.roleperms import RolePerms
    from modobot.models.usermute import UserMute

    logging.info("Setting all roles")
    for guild in modobot_client.guilds:
        if guild.name == SERVER_NAME:
            for role in guild.roles:
                if role.name == "@everyone":
                    continue
                try:
                    RolePerms.create(name=role.name)
                except IntegrityError:
                    logging.debug(f"Role {role.name} already exists, skipping")
                    pass
                else:
                    logging.debug(f"Added role {role.name}")
    logging.info("All roles created")
    logging.info("Checking timers for muted members")
    for usermute in UserMute.select().where((UserMute.is_unmuted == False)):  # noqa
        if not usermute.dt_unmute:
            logging.info(f"Mute {usermute.id} doesn't have unmute time, skipping")
            continue
        logging.info(f"Added reset mute for {usermute.id}")
        modobot_client.loop.create_task(
            unmute_user_after(
                usermute, skip=True if usermute.dt_unmute < datetime.now() else False
            )
        )


from modobot.models.userban import UserBan, UserBan_Admin
from modobot.models.userwarn import UserWarn, UserWarn_Admin
from modobot.models.usernote import UserNote, UserNote_Admin
from modobot.models.usermute import UserMute, UserMute_Admin
from modobot.models.actionlog import ActionLog, ActionLog_Admin
from modobot.models.roleperms import RolePerms, RolePerms_Admin
from modobot.models.adminuser import AdminUser, AdminUser_Admin
from modobot.models.unautorized_report import (
    UnauthorizedReport,
    UnauthorizedReport_Admin,
)

logging.info("Creating tables")
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
if not UserMute.table_exists():
    UserMute.create_table()
if not UnauthorizedReport.table_exists():
    UnauthorizedReport.create_table()

logging.info("Registering commands")
import modobot.utils.checks  # noqa
import modobot.commands.ban  # noqa
import modobot.commands.clear  # noqa
import modobot.commands.warn  # noqa
import modobot.commands.note  # noqa
import modobot.commands.search  # noqa
import modobot.commands.lock  # noqa
import modobot.commands.info  # noqa
import modobot.commands.mute  # noqa


from modobot.routes.admin import AdminIndexView, NewAdminView, ChangePasswordView

# Creates the Admin manager
logging.info("Registering admin manager")
admin = Admin(
    application,
    name="Among Us France Discord Admin",
    template_mode="bootstrap4",
    index_view=AdminIndexView(),
    base_template="admin/admin_master.html",
)

# Registers the views for each table
logging.info("Registering admin views")
admin.add_view(AdminUser_Admin(AdminUser, name="Admins"))
admin.add_view(RolePerms_Admin(RolePerms, name="Permissions"))
admin.add_view(ActionLog_Admin(ActionLog, name="Log"))
admin.add_view(
    UnauthorizedReport_Admin(UnauthorizedReport, name="Unauthorized commands")
)
admin.add_view(UserWarn_Admin(UserWarn, name="Avertissements", category="Actions"))
admin.add_view(UserNote_Admin(UserNote, name="Notes", category="Actions"))
admin.add_view(UserBan_Admin(UserBan, name="Bans", category="Actions"))
admin.add_view(UserMute_Admin(UserMute, name="Mutes", category="Actions"))
admin.add_view(NewAdminView(name="New Admin", endpoint="register_admin"))
admin.add_view(ChangePasswordView(name="Change password", endpoint="change_password"))
