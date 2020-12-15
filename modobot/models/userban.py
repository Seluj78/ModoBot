from datetime import datetime

from peewee import CharField
from peewee import DateTimeField
from peewee import BooleanField

from modobot.models import BaseModel


class UserBan(BaseModel):
    banned_id = CharField(null=False)
    dt_banned = DateTimeField(default=datetime.utcnow)
    moderator_id = CharField(null=False)
    reason = CharField(null=False)
    is_unbanned = BooleanField(default=False)
