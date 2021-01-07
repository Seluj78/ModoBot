from flask_admin.contrib.peewee import ModelView
from flask_login import current_user
from peewee import CharField
from peewee import ForeignKeyField

from modobot.models import BaseModel
from modobot.models import UnsignedBitIntegerField
from modobot.models.guildsettings import GuildSettings
from modobot.models.rolecategory import RoleCategory


class Role(BaseModel):
    role_name = CharField(null=False)
    role_id = UnsignedBitIntegerField(null=False)
    guild = ForeignKeyField(GuildSettings, backref="roles", unique=False)
    category = ForeignKeyField(RoleCategory, backref="roles", unique=False)


class Role_Admin(ModelView):
    model_class = Role

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
