from flask_admin.contrib.peewee import ModelView
from flask_login import current_user
from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField

from modobot.models import BaseModel
from modobot.models.guildsettings import GuildSettings
from modobot.utils.france_datetime import datetime_now_france


class UserBan(BaseModel):
    banned_id = CharField(null=False)
    banned_name = CharField(null=False)
    dt_banned = DateTimeField(default=datetime_now_france)
    moderator_id = CharField(null=False)
    moderator_name = CharField(null=False)
    reason = CharField(null=False)
    is_unbanned = BooleanField(default=False)
    dt_unbanned = DateTimeField(null=True)
    guild = ForeignKeyField(GuildSettings, backref="userbans", unique=False)


class UserBan_Admin(ModelView):
    model_class = UserBan
    column_default_sort = ("dt_banned", True)

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
