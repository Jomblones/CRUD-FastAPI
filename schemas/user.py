from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    password: str
    
class Books(BaseModel):
    book_name: str
    book_category: str
    book_author: str
    