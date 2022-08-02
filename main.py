
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from routes.index import user
from routes.index import book


app = FastAPI()

app.include_router(user)
app.include_router(book)


