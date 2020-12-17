from flask_admin.contrib.peewee import ModelView
from flask_login import current_user
from peewee import CharField
from peewee import DateTimeField

from modobot.models import BaseModel
from modobot.utils.france_datetime import datetime_now_france

ACTION_TYPES = [
    ("permissions", "permissions"),
    ("channel", "channel"),
    ("staff_action", "staff_action"),
    ("bot_action", "bot_action"),
]


class UnauthorizedReport(BaseModel):
    moderator_name = CharField(null=False)
    moderator_id = CharField(null=False)
    command = CharField(null=False)
    dt_action = DateTimeField(default=datetime_now_france)
    type = CharField(null=False, choices=ACTION_TYPES)


class UnauthorizedReport_Admin(ModelView):
    model_class = UnauthorizedReport
    column_default_sort = ("dt_action", True)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
