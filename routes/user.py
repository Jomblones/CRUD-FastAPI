from fastapi import APIRouter, Request, Response, status, Form
from fastapi.templating import Jinja2Templates
from config.db import conn
from models.user import users
from schemas.index import User
user = APIRouter()

templates = Jinja2Templates(directory="templates")

#Read All data 
@user.get("/")
async def read_data(request: Request):
    datas = conn.execute(users.select()).fetchall() 
    context = {'request':request, 'datas': datas}
    return templates.TemplateResponse("index.html", context)

#Add data
@user.post("/add")
async def write_data(user:User, response:Response, request:Request):
    
    conn.execute(users.insert().values(
        name=user.name,
        email=user.email,
        password=user.password
    ))
    response = {"msg":"Data berhasil ditambahkan"
                }
    context = {'request':request}
    return templates.TemplateResponse("add_user.html", context)

#Edit data by ID
@user.put("/{id}")
async def update_data(id:int, user:User):
    conn.execute(users.update().values(
        name=user.name,
        email=user.email,
        password=user.password
    ).where(users.c.id == id) )
    return conn.execute(users.select()).fetchall()

#Delete data by ID
@user.delete("/{id}")
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
