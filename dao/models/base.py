from peewee import Model

from dao.connections import db


class BaseModel(Model):
    class Meta:
        database = db
