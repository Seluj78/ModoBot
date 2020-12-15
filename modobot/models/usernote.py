from datetime import datetime

from peewee import CharField
from peewee import DateTimeField

from modobot.models import BaseModel


class UserNote(BaseModel):
    noted_id = CharField(null=False)
    dt_noted = DateTimeField(default=datetime.utcnow)
    moderator_id = CharField(null=False)
    reason = CharField(null=False)
