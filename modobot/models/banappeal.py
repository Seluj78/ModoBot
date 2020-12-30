from flask_admin.contrib.peewee import ModelView
from flask_login import current_user
from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import TextField

from modobot.models import BaseModel
from modobot.models.userban import UserBan
from modobot.utils.france_datetime import datetime_now_france


class BanAppeal(BaseModel):
    dt_requested = DateTimeField(default=datetime_now_france)
    ban = ForeignKeyField(UserBan, backref="banappeals", unique=True)
    appeal_reason = TextField(null=False)
    result = CharField(
        null=True, choices=[("accepted", "accepted"), ("rejected", "rejected")]
    )
    is_resolved = BooleanField(default=False)


class BanAppeal_Admin(ModelView):
    model_class = BanAppeal
    column_default_sort = ("dt_requested", True)

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
