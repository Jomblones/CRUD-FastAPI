from fastapi import APIRouter, Request, Response, status, Form
from fastapi.templating import Jinja2Templates
from config.db import conn
from models.index import users
from schemas.index import User

from models.index import books
from schemas.index import Books

user = APIRouter()
book = APIRouter()

# USER
#Read All data 
@user.get("/user/get")
async def read_data(request: Request):
    datas = conn.execute(users.select()).fetchall() 
    context = {'request':request, 'datas': datas}
    return datas

#Add data
@user.post("/user/add")
async def write_data(user:User, response:Response, request:Request):

    conn.execute(users.insert().values(
        name=user.name,
        email=user.email,
        password=user.password
    ))
    response = {"msg":"Data berhasil ditambahkan"
                }
    datas = conn.execute(users.select()).fetchall() 
    return datas

#Edit data by ID
@user.put("/user/update-{id}")
async def update_data(id:int, user:User):
    conn.execute(users.update().values(
        name=user.name,
        email=user.email,
        password=user.password
    ).where(users.c.id == id) )
    return conn.execute(users.select()).fetchall()

#Delete data by ID
@user.delete("/user/delete-{id}")
async def delete_data(id:int, response: Response):
    query = users.select().where(users.c.id == id)
    data = conn.execute(query).fetchone()
    if data is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": "data tidak ditemukan",
                "status": response.status_code}
        
    conn.execute(users.delete().where(users.c.id == id))
    response = {"msg": f"Sukses menghapus data dengan id {id}"}
    return response

