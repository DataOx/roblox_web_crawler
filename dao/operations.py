from dao.connections import db

from dao.models import ExtractProduct


def initialize():
    with db as connected_db:
        connected_db.create_tables([ExtractProduct], safe=True)


def create_extract_product(**queries) -> ExtractProduct:
    with db.atomic():
        obj = ExtractProduct.create(**queries)
        obj.save()
    return obj


def get_scraped_data_roblox():
    with db:
        for obj in ExtractProduct.select():
            yield obj
        # for i in objs:
        #     print(i.id)


# if __name__ == '__main__':
#     # migration()
#     for scraped_data in get_scraped_data_roblox():
#         print(scraped_data.url, scraped_data.name, str(scraped_data.created), str(scraped_data.updated),
#               scraped_data.visits, scraped_data.badges_total, scraped_data.favorites, scraped_data.message)
