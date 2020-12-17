import datetime
import re

from discord.ext import commands

from modobot.utils.errors import IncorrectTimeError
from modobot.utils.france_datetime import datetime_now_france


class TimeConverter(commands.Converter):
    async def convert(self, ctx, time):
        matches = re.fullmatch("(\d+)([mhd])", time)  # noqa
        if not matches:
            raise IncorrectTimeError("Doit être `0000m/h/d`")
        count = int(matches[1])
        s_type = matches[2]

        if s_type == "m":
            delta = datetime.timedelta(minutes=count)
        elif s_type == "h":
            delta = datetime.timedelta(hours=count)
        elif s_type == "d":
            delta = datetime.timedelta(days=count)
        else:
            raise IncorrectTimeError("Doit être `0000m/h/d`")

        dt_unmute = datetime_now_france() + delta
        return dt_unmute
