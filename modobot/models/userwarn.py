from datetime import datetime

from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField

from modobot.models import BaseModel


class UserWarn(BaseModel):
    warned_id = CharField(null=False)
    dt_warned = DateTimeField(default=datetime.utcnow)
    moderator_id = CharField(null=False)
    reason = CharField(null=False)
    is_unwarned = BooleanField(default=False)
    dt_unwarned = DateTimeField(default=datetime.utcnow)
