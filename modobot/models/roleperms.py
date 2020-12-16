from flask_admin.contrib.peewee import ModelView
from flask_login import current_user
from peewee import BooleanField
from peewee import CharField

from modobot.models import BaseModel


class RolePerms(BaseModel):
    name = CharField(null=False, unique=True)
    silence_notif = BooleanField(default=True)
    can_ban = BooleanField(default=True)
    can_unban = BooleanField(default=False)
    can_warn = BooleanField(default=True)
    can_note = BooleanField(default=True)
    can_search = BooleanField(default=True)
    can_clear = BooleanField(default=False)
    can_lock = BooleanField(default=False)
    can_unlock = BooleanField(default=False)
    can_info = BooleanField(default=True)


class RolePerms_Admin(ModelView):
    model_class = RolePerms

    def is_accessible(self):
        return current_user.is_authenticated
