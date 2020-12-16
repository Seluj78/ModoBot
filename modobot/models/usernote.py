from flask_admin.contrib.peewee import ModelView
from flask_login import current_user
from peewee import CharField
from peewee import DateTimeField

from modobot.models import BaseModel
from modobot.utils.france_datetime import datetime_now_france


class UserNote(BaseModel):
    noted_id = CharField(null=False)
    dt_noted = DateTimeField(default=datetime_now_france)
    moderator_id = CharField(null=False)
    reason = CharField(null=False)


class UserNote_Admin(ModelView):
    model_class = UserNote
    column_default_sort = ("dt_noted", True)

    def is_accessible(self):
        return current_user.is_authenticated
