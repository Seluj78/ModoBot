from peewee import Model

from modobot import modo_db


class BaseModel(Model):
    class Meta:
        database = modo_db  # type: ignore
