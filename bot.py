import logging

from modobot import modobot_client
from modobot.static import BOT_TOKEN
from modobot.utils.logging import setup_logging

if __name__ == "__main__":
    setup_logging()
    logging.getLogger("discord").setLevel(logging.WARNING)
    modobot_client.run(BOT_TOKEN)
