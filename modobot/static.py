import os

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


ROOT_PATH = os.path.join(os.path.dirname(__file__), "../")

BOT_TOKEN = os.getenv("BOT_TOKEN")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
COMMAND_CHANNEL_ID = os.getenv("COMMAND_CHANNEL_ID")
SERVER_URL = os.getenv("SERVER_URL")
