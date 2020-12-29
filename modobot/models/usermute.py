from flask_admin.contrib.peewee import ModelView
from flask_login import current_user
from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField

from modobot.models import BaseModel
from modobot.utils.france_datetime import datetime_now_france


class UserMute(BaseModel):
    muted_id = CharField(null=False)
    muted_name = CharField(null=False)
    dt_muted = DateTimeField(default=datetime_now_france)
    moderator_id = CharField(null=False)
    moderator_name = CharField(null=False)
    reason = CharField(null=False)
    is_unmuted = BooleanField(default=False)
    dt_unmute = DateTimeField(null=True)
    user_roles = CharField(null=False)


class UserMute_Admin(ModelView):
    model_class = UserMute
    column_default_sort = ("dt_muted", True)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
