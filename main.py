from fastapi import FastAPI 

from routes.index import index


app = FastAPI()

app.include_router(index)
