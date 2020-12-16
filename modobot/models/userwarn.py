from flask_admin.contrib.peewee import ModelView
from flask_login import current_user
from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField

from modobot.models import BaseModel
from modobot.utils.france_datetime import datetime_now_france


class UserWarn(BaseModel):
    warned_id = CharField(null=False)
    dt_warned = DateTimeField(default=datetime_now_france)
    moderator_id = CharField(null=False)
    reason = CharField(null=False)
    is_unwarned = BooleanField(default=False)
    dt_unwarned = DateTimeField(default=datetime_now_france)


class UserWarn_Admin(ModelView):
    model_class = UserWarn

    def is_accessible(self):
        return current_user.is_authenticated
