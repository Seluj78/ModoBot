from modobot.models import BaseModel
from peewee import DateTimeField, CharField
from datetime import datetime


class UserBan(BaseModel):
    banned_id = CharField(null=False)
    dt_banned = DateTimeField(default=datetime.utcnow)
    moderator_id = CharField(null=False)
    reason = CharField(null=False)
