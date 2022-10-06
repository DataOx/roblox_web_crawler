from peewee import PostgresqlDatabase

from config import DATABASE_URL


db = PostgresqlDatabase(DATABASE_URL)
