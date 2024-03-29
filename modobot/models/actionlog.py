from flask_admin.contrib.peewee import ModelView
from flask_login import current_user
from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField

from modobot.models import BaseModel
from modobot.models.guildsettings import GuildSettings
from modobot.utils.france_datetime import datetime_now_france

ACTION_TYPES = [
    ("ban", "ban"),
    ("unban", "unban"),
    ("warn", "warn"),
    ("note", "note"),
    ("clear", "clear"),
    ("search", "search"),
    ("lock", "lock"),
    ("unlock", "unlock"),
    ("mute", "mute"),
    ("unmute", "unmute"),
    ("addcat", "addcat"),
]


class ActionLog(BaseModel):
    moderator_name = CharField(null=False)
    moderator_id = CharField(null=False)
    user_name = CharField()
    user_id = CharField()
    dt_action = DateTimeField(default=datetime_now_france)
    action = CharField(null=False, choices=ACTION_TYPES)
    comments = CharField()
    guild = ForeignKeyField(GuildSettings, backref="actionlogs", unique=False)


class ActionLog_Admin(ModelView):
    model_class = ActionLog
    column_default_sort = ("dt_action", True)

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
        return current_user.is_authenticated
