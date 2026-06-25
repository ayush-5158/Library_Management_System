from pydantic import BaseModel
from typing import Optional

class Books(BaseModel):
    title : str
    author : str
    is_available : Optional[str] = "Yes"
    assigned_to : Optional[str] ="None"

class BookUpdate(BaseModel):
    title : Optional[str] = None
    author : Optional[str] = None
    is_available: Optional[str] = None
    assigned_to : Optional[str] = None

class Student(BaseModel):
    name : str
    grade : str
    email : str
    phone_number:str

class StudentUpdate(BaseModel):
    name : Optional[str] = None
    grade : Optional[str] = None
    email : Optional[str] = None
    phone_number:Optional[str] = None

class IssuedBook(BaseModel):
    book_id : int
    name : str
    issued_date : str
    return_date:str
    student_id :int

class IssuedBookUpdate(BaseModel):
    book_id : Optional[int] = None
    name : Optional[str] = None
    issued_date : Optional[str] = None
    return_date:Optional[str] = None
    student_id :Optional[int] = None

class Complaint(BaseModel):
    student_id :Optional[int] = None
    complaint : Optional[str] = None
    complaint_date : Optional[str] = None
    resolve_date : Optional[str] = None