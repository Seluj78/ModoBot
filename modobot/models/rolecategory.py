from flask_admin.contrib.peewee import ModelView
from flask_login import current_user
from peewee import BooleanField
from peewee import CharField
from peewee import ForeignKeyField
from peewee import IntegerField

from modobot.models import BaseModel
from modobot.models.guildsettings import GuildSettings


class RoleCategory(BaseModel):
    name = CharField(null=False)
    guild = ForeignKeyField(GuildSettings, backref="rolecategories", unique=False)
    position = IntegerField(default=0, null=False)
    can_ban = BooleanField(default=True)
    can_unban = BooleanField(default=False)
    can_warn = BooleanField(default=True)
    can_note = BooleanField(default=True)
    can_search = BooleanField(default=True)
    can_clear = BooleanField(default=True)
    can_lock = BooleanField(default=False)
    can_unlock = BooleanField(default=False)
    can_mute = BooleanField(default=True)
    can_unmute = BooleanField(default=True)
    can_punish_staff = BooleanField(default=False)


class RoleCategory_Admin(ModelView):
    model_class = RoleCategory

    @property
    def can_edit(self):
        return current_user.is_admin

    @property
    def can_create(self):
        return current_user.is_admin

    @property
    def can_delete(self):
        return current_user.is_admin

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
