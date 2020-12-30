from flask_admin.contrib.peewee import ModelView
from flask_login import current_user
from peewee import BooleanField
from peewee import CharField
from peewee import ForeignKeyField

from modobot.models import BaseModel
from modobot.models import UnsignedBitIntegerField
from modobot.models.guildsettings import GuildSettings


class RolePerms(BaseModel):
    role_name = CharField(null=False)
    role_id = UnsignedBitIntegerField(null=False)
    guild = ForeignKeyField(GuildSettings, backref="roleperms", unique=False)
    is_staff = BooleanField(default=False)
    silence_notif = BooleanField(default=True)
    can_ban = BooleanField(default=False)
    can_unban = BooleanField(default=False)
    can_warn = BooleanField(default=False)
    can_note = BooleanField(default=False)
    can_search = BooleanField(default=False)
    can_clear = BooleanField(default=False)
    can_lock = BooleanField(default=False)
    can_unlock = BooleanField(default=False)
    can_mute = BooleanField(default=False)
    can_unmute = BooleanField(default=False)
    can_punish_staff = BooleanField(default=False)


class RolePerms_Admin(ModelView):
    model_class = RolePerms

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
