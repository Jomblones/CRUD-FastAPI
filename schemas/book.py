from pydantic import BaseModel

class Books(BaseModel):
    title: str
    category: str
    author: str
    