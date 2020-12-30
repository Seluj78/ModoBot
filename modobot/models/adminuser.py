from flask_admin.contrib.peewee import ModelView
from flask_login import current_user
from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import TextField

from modobot.models import BaseModel
from modobot.utils.france_datetime import datetime_now_france


class AdminUser(BaseModel):
    username = CharField(
        null=False, help_text="Username of admin user", verbose_name="Username"
    )
    email = CharField(null=False, help_text="Email of admin user", verbose_name="Email")
    password = TextField(
        null=False, help_text="Hashed password of admin user", verbose_name="Password"
    )
    dt_added = DateTimeField(
        null=False,
        default=datetime_now_france,
        help_text="When was the admin user entry added",
        verbose_name="Datetime Added",
    )
    discord_id = CharField(
        null=False, help_text="Your discord ID", verbose_name="Discord ID"
    )
    is_admin = BooleanField(default=False)

    def get_id(self) -> int:
        return int(self.id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    # Required for administrative interface
    def __unicode__(self):
        return self.username


class AdminUser_Admin(ModelView):
    model_class = AdminUser

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
