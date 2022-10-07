import peewee as pw

from dao.models.base import BaseModel
from utils import get_pacific_time


class ExtractProduct(BaseModel):
    url = pw.TextField(verbose_name='URL')
    row_index = pw.IntegerField()  # row index in spreadsheet
    name = pw.CharField(null=True)
    created = pw.DateTimeField(verbose_name='creation date', null=True)
    updated = pw.DateTimeField(verbose_name='most recent update date', null=True)
    visits = pw.BigIntegerField(default=0)
    favorites = pw.BigIntegerField(default=0)
    badges_total = pw.BigIntegerField(default=0)
    message = pw.TextField(null=True)
    created_at = pw.DateTimeField(default=get_pacific_time)
