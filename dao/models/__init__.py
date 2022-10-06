from peewee import OperationalError

from dao.connections import db
from dao.models.base import BaseModel
from dao.models.extract_product import ExtractProduct


def initialize():
    for _ in range(25):
        try:
            connection = db.connect()
        except OperationalError:
            continue
        else:
            ExtractProduct.create_table()
             # add another models here
            connection.close()
