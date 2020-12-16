from flask_admin.contrib.peewee import ModelView
from flask_login import current_user
from peewee import CharField
from peewee import DateTimeField

from modobot.models import BaseModel
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
    ("info", "info"),
    ("mute", "mute"),
    ("unmute", "unmute"),
]


class ActionLog(BaseModel):
    moderator = CharField(null=False)
    user = CharField()
    dt_action = DateTimeField(default=datetime_now_france)
    action = CharField(null=False, choices=ACTION_TYPES)
    comments = CharField()


class ActionLog_Admin(ModelView):
    model_class = ActionLog
    column_default_sort = ("dt_action", True)
    can_create = False
    can_edit = False
    can_delete = False

    def is_accessible(self):
        return current_user.is_authenticated
