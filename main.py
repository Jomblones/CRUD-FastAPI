
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from routes.index import user

app = FastAPI()

app.include_router(user)



