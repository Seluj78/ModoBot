from flask_admin.contrib.peewee import ModelView
from flask_login import current_user
from peewee import CharField

from modobot.models import BaseModel
from modobot.models import UnsignedBitIntegerField


class GuildSettings(BaseModel):
    guild_name = CharField(null=False, unique=True)
    guild_id = UnsignedBitIntegerField(null=False, unique=True)
    muted_role_id = UnsignedBitIntegerField(null=False)
    archive_channel_id = UnsignedBitIntegerField(null=False)
    master_user_id = UnsignedBitIntegerField(null=False)


class GuildSettings_Admin(ModelView):
    model_class = GuildSettings

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
