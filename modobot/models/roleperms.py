from peewee import BooleanField
from peewee import CharField

from modobot.models import BaseModel


class RolePerms(BaseModel):
    name = CharField(null=False)
    can_ban = BooleanField(default=True)
    can_unban = BooleanField(default=False)
    can_warn = BooleanField(default=True)
    can_note = BooleanField(default=True)
    can_search = BooleanField(default=True)
    can_clear = BooleanField(default=False)
