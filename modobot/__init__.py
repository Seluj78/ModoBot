import os

import peewee
from dotenv import load_dotenv
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
    "BOT_TOKEN"
]

for item in REQUIRED_ENV_VARS:
    if item not in os.environ:
        raise EnvironmentError(f"{item} is not set in the server's environment or .env file. It is required.")

from modobot.static import (
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_PORT,
    DB_HOST,
    BOT_TOKEN,
)

setup_logging()

modo_db = peewee.MySQLDatabase(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)

from modobot.models.userban import UserBan

if not UserBan.table_exists():
    UserBan.create_table()
