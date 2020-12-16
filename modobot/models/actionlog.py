from datetime import datetime

from peewee import CharField
from peewee import DateTimeField

from modobot.models import BaseModel


ACTION_TYPES = [
    ("ban", "ban"),
    ("unban", "unban"),
    ("warn", "warn"),
    ("note", "note"),
    ("clear", "clear"),
    ("search", "search"),
    ("lock", "lock"),
    ("unlock", "unlock"),
    ("info", "info"),
]


class ActionLog(BaseModel):
    moderator_id = CharField(null=False)
    user_id = CharField()
    dt_action = DateTimeField(default=datetime.utcnow())
    action = CharField(null=False, choices=ACTION_TYPES)
    comments = CharField()
