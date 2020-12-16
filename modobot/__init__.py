import logging
import os

import peewee
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from peewee import DoesNotExist
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
    "FLASK_SECRET_KEY",
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


from modobot.models.userban import UserBan, UserBan_Admin
from modobot.models.userwarn import UserWarn, UserWarn_Admin
from modobot.models.usernote import UserNote, UserNote_Admin
from modobot.models.actionlog import ActionLog, ActionLog_Admin
from modobot.models.roleperms import RolePerms, RolePerms_Admin
from modobot.models.adminuser import AdminUser, AdminUser_Admin

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


# from afpy.routes.home import home_bp
#
# application.register_blueprint(home_bp)


from modobot.routes.admin import AdminIndexView, NewAdminView, ChangePasswordView

# Creates the Admin manager
admin = Admin(
    application,
    name="Among Us France Discord Admin",
    template_mode="bootstrap4",
    index_view=AdminIndexView(),
    base_template="admin/admin_master.html",
)

# Registers the views for each table
admin.add_view(AdminUser_Admin(AdminUser))
admin.add_view(UserWarn_Admin(UserWarn))
admin.add_view(UserNote_Admin(UserNote))
admin.add_view(ActionLog_Admin(ActionLog))
admin.add_view(RolePerms_Admin(RolePerms))
admin.add_view(UserBan_Admin(UserBan))
admin.add_view(NewAdminView(name="New Admin", endpoint="register_admin"))
admin.add_view(ChangePasswordView(name="Change password", endpoint="change_password"))
