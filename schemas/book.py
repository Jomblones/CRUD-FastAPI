from pydantic import BaseModel

class Books(BaseModel):
    book_name: str
    book_category: str
    book_author: str
    