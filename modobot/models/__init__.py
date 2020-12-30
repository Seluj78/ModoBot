from peewee import BigIntegerField
from peewee import Model

from modobot import modo_db


class BaseModel(Model):
    class Meta:
        database = modo_db  # type: ignore


class UnsignedBitIntegerField(BigIntegerField):
    field_type = "bigint unsigned"
