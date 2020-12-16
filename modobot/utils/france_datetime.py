from datetime import datetime
from functools import partial
from zoneinfo import ZoneInfo

datetime_now_france = partial(datetime.now, tz=ZoneInfo("Europe/Paris"))

__all__ = ["datetime_now_france"]
