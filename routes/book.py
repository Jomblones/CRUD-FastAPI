from fastapi import APIRouter, Request, Response, status, Form
from fastapi.templating import Jinja2Templates
from config.db import conn
from models.index import books
from schemas.index import Books

book = APIRouter()

# BOOK
#Read All data 
@book.get("/book/get")
async def read_data(request: Request):
    datas = conn.execute(books.select()).fetchall() 
    context = {'request':request, 'datas': datas}
    return datas

#Add data
@book.post("/book/add")
async def write_data(book: Books, response:Response, request:Request):
    query = books.select().where(books.c.id == id)
    conn.execute(books.insert().values(
        book_name=book.book_name,
        book_category=book.book_category,
        book_author=book.book_author
    ))
    response = {"msg":"Data berhasil ditambahkan"
                }
    datas = conn.execute(books.select()).fetchall() 
    return datas

#Edit data by ID
@book.put("/book/update-{id}")
async def update_data(id:int, book:Books,response: Response):

    query = books.select().where(books.c.id == id)
    data = conn.execute(query).fetchone()
    if data is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": "data tidak ditemukan",
                "status": response.status_code}
    else :
        conn.execute(books.update().values(
            book_name=book.book_name,
            book_category=book.book_category,
            book_author=book.book_author
        ).where(books.c.id == id) )
    return conn.execute(books.select()).fetchall()

#Delete data by ID
@book.delete("/book/delete-{id}")
async def delete_data(id:int, response: Response):
    query = books.select().where(books.c.id == id)
    data = conn.execute(query).fetchone()
    if data is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": "data tidak ditemukan",
                "status": response.status_code}
        
    conn.execute(books.delete().where(books.c.id == id))
    response = {"msg": f"Sukses menghapus data dengan id {id}"}
    return response
