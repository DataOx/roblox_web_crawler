from playhouse.postgres_ext import PostgresqlExtDatabase

from config import POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_PORT, POSTGRES_HOST


db = PostgresqlExtDatabase(database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_HOST,
                           port=POSTGRES_PORT)
