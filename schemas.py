from pydantic import BaseModel
from typing import Optional
from datetime import date

class BookCreate(BaseModel):
    title : str
    author : str

class BookUpdate(BaseModel):
    title : Optional[str] = None
    author : Optional[str] = None

class User(BaseModel):
    name : str
    role : str
    email : str
    phone_number:str
    password:str

class UserResponse(BaseModel):
    student_id : int
    name: str
    role :str
    email :str
    phone_number:str

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name : Optional[str] = None
    role : Optional[str] = None
    email : Optional[str] = None
    phone_number:Optional[str] = None

class IssuedBook(BaseModel):
    book_id : int
    student_id :int
    issue_date : date
    return_date : Optional[date] = None


class IssuedBookResponse(BaseModel):
    issue_id : int
    book_id : int
    student_id : int
    issue_date : date

    class Config:
        from_attributes = True


class IssuedBookUpdate(BaseModel):
    issue_id : int
    return_date: date

    class Config:
        from_attributes = True
    
class LoginRequest(BaseModel):
    email : str
    password : str

