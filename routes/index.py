from typing import Mapping
from fastapi import APIRouter

from fastapi import APIRouter, Depends, HTTPException, status, Response, status 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import null, true, values

from config.db import conn
from models.index import users, books
from schemas.index import User, Books
import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='CrudFastApi',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)



index = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#Login
@index.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    sql_user = '''SELECT name FROM user WHERE name =%s'''
    username_data = conn.execute(sql_user, str(form_data.username)).fetchone()

    sql_pass = '''SELECT password FROM user WHERE name =%s'''
    password_data = conn.execute(sql_pass, form_data.username).fetchone()
    
    verify_username = username_data[0] == form_data.username
    verify_pass = password_data[0] == form_data.password
    
    if verify_username == True and verify_pass == True:
        return {
            "access_token" : form_data.username,
            "detail":"authenticated",
            "token_type": "bearer"
            }
    else:
        # return {
        #     "username":verify_username,
        #     "password":verify_pass,
        #     "user":username_data,
        #     "pass":password_data
        # }
        raise HTTPException(status_code=400, detail="Incorrect Password/Username")
        
#Register 
@index.post("/register")
async def register(user:User):

    conn.execute(users.insert().values(
        name=user.name,
        email=user.email,
        password=user.password
    ))
    response = {"msg":"Register Successfull"
                }
    
    return response
    
# USER
#Read All data 
@index.get("/user/get")
async def read_user_data(token: str = Depends(oauth2_scheme)):
    datas = conn.execute(users.select()).fetchall() 
    return datas

#Add data
@index.post("/user/add")
async def write_user_data(user:User, token: str = Depends(oauth2_scheme)):

    conn.execute(users.insert().values(
        name=user.name,
        email=user.email,
        password=user.password
    ))
    response = {"msg":"Data berhasil ditambahkan"}
    
    datas = conn.execute(users.select()).fetchall() 
    return datas
    
# Edit data by ID
@index.put("/user/update-{id}")
async def update_user_data(id:int,user:User, response:Response, token: str = Depends(oauth2_scheme)):
    query = users.select().where(users.c.id == id)
    data = conn.execute(query).fetchone()    
    if data is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": "data tidak ditemukan",
                "status": response.status_code}
    else :
        conn.execute(users.update().values(
            name=user.name,
            email=user.email,
            password=user.password).where(users.c.id == id))
    response = {"msg": f"Sukses mengubah data dengan id {id}"}
    datas=conn.execute(users.select()).fetchall()
    return response, datas

#Delete data by ID
@index.delete("/user/delete-{id}")
async def delete_user_data(id:int, response:Response ,token: str = Depends(oauth2_scheme)):
    query = users.select().where(users.c.id == id)
    data = conn.execute(query).fetchone()
    if data is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": "data tidak ditemukan",
                "status": response.status_code}
        
    conn.execute(users.delete().where(users.c.id == id))
    response = {"msg": f"Sukses menghapus data dengan id {id}"}
    datas=conn.execute(users.select()).fetchall()
    return response, datas


# BOOKS
#Read All data 
@index.get("/book/get")
async def get_book_data(token: str = Depends(oauth2_scheme)):
    datas = conn.execute(books.select()).fetchall() 
    return datas

#Add data
@index.post("/book/add")
async def write_book_data(book: Books, token: str = Depends(oauth2_scheme)):
    conn.execute(books.insert().values(
        title=book.title,
        category=book.category,
        author=book.author
    ))
    response = {"msg":"Data berhasil ditambahkan"
                }
    datas = conn.execute(books.select()).fetchall() 
    return response, datas

#Edit data by ID
@index.put("/book/update-{id}")
async def update_book_data(id:int, book:Books, response:Response ,token: str = Depends(oauth2_scheme)):

    query = books.select().where(books.c.id == id)
    data = conn.execute(query).fetchone()
    if data is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": "data tidak ditemukan",
                "status": response.status_code}
    else :
        conn.execute(books.update().values(
            title=book.title,
            category=book.category,
            author=book.author
        ).where(books.c.id == id) )
        response = {"msg": f"Sukses menghapus data dengan id {id}"}
    datas=conn.execute(books.select()).fetchall()
    return response, datas

#Delete data by ID
@index.delete("/book/delete-{id}")
async def delete_book_data(id:int, response: Response,token: str = Depends(oauth2_scheme) ):
    query = books.select().where(books.c.id == id)
    data = conn.execute(query).fetchone()
    if data is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": "data tidak ditemukan",
                "status": response.status_code}
        
    conn.execute(books.delete().where(books.c.id == id))
    response = {"msg": f"Sukses menghapus data dengan id {id}"}
    datas=conn.execute(books.select()).fetchall()
    return response, datas

#Show data by ID
@index.get("/book/get-{id}")
async def get_data_by_ID(id:int, response: Response,token: str = Depends(oauth2_scheme) ):
    query = books.select().where(books.c.id == id)
    data = conn.execute(query).fetchone()
    if data is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": "data tidak ditemukan",
                "status": response.status_code}
        
    result = conn.execute(books.select().where(books.c.id == id)).fetchone()
    return result
