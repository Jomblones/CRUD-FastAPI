from sqlalchemy import Table, Column
from config.db import meta
from sqlalchemy.sql.sqltypes import Integer, String

books = Table(
    'book', meta,
    Column('id', Integer, primary_key=True),
    Column('book_name', String(255)),
    Column('book_category', String(255)),
    Column('book_author', String(255))
)
