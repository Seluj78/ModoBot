from datetime import datetime

from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField

from modobot.models import BaseModel


class UserBan(BaseModel):
    banned_id = CharField(null=False)
    dt_banned = DateTimeField(default=datetime.utcnow)
    moderator_id = CharField(null=False)
    reason = CharField(null=False)
    is_unbanned = BooleanField(default=False)
    dt_unbanned = DateTimeField(default=datetime.utcnow)
