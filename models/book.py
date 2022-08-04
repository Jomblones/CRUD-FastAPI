from sqlalchemy import Table, Column
from config.db import meta
from sqlalchemy.sql.sqltypes import Integer, String

books = Table(
    'book', meta,
    Column('id', Integer, primary_key=True),
    Column('title', String(255)),
    Column('category', String(255)),
    Column('author', String(255))
)
