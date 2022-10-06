from dao.connections import db
from dao.models.base import BaseModel
from dao.models.extract_product import ExtractProduct


def initialize():
    with db:
        ExtractProduct.create_table()
        # add another models here
