from datetime import datetime
from functools import partial
from zoneinfo import ZoneInfo

datetime_now_france = partial(datetime.now, tz=ZoneInfo("Europe/Paris"))


def clean_format(dt: datetime) -> str:
    return dt.strftime("%A %d %b %Y à %H:%M:%S")


__all__ = ["datetime_now_france", "clean_format"]
