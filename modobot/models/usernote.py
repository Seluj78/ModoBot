from flask_admin.contrib.peewee import ModelView
from flask_login import current_user
from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField

from modobot.models import BaseModel
from modobot.models.guildsettings import GuildSettings
from modobot.utils.france_datetime import datetime_now_france


class UserNote(BaseModel):
    noted_id = CharField(null=False)
    noted_name = CharField(null=False)
    dt_noted = DateTimeField(default=datetime_now_france)
    moderator_id = CharField(null=False)
    moderator_name = CharField(null=False)
    reason = CharField(null=False)
    guild = ForeignKeyField(GuildSettings, backref="usernotes", unique=False)


class UserNote_Admin(ModelView):
    model_class = UserNote
    column_default_sort = ("dt_noted", True)

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
