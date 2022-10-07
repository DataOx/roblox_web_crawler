from dao.connections import db

from dao.models import ExtractProduct


def create_extract_product(**queries) -> ExtractProduct:
    with db.atomic():
        obj = ExtractProduct.create(**queries)
        obj.save()
    return obj
