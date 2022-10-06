from peewee import PostgresqlDatabase

from config import POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_PORT, POSTGRES_HOST


db = PostgresqlDatabase(POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_HOST,
                        port=POSTGRES_PORT, autoconnect=False, autocommit=False)
