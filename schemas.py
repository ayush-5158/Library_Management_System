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
    password:str

class StudentResponse(BaseModel):
    student_id : int
    name: str
    grade :str
    email :str
    phone_number:str

    class Config:
        from_attributes = True

class StudentUpdate(BaseModel):
    name : Optional[str] = None
    grade : Optional[str] = None
    email : Optional[str] = None
    phone_number:Optional[str] = None

class IssuedBook(BaseModel):
    book_id : int
    student_id :int
    issue_date : str
    return_date : Optional[str] = None


class IssuedBookResponse(BaseModel):
    issue_id : int
    book_id : int
    student_id : int
    issue_date : str

    class Config:
        from_attributes = True


class IssuedBookUpdate(BaseModel):
    issue_id : int
    return_date: str

    class Config:
        from_attributes = True

class Complaint(BaseModel):
    student_id :Optional[int] = None
    complaint : Optional[str] = None
    complaint_date : Optional[str] = None
    resolved_date : Optional[str] = None


class ComplaintUpdate(BaseModel):
    complaint : Optional[str] = None
    resolved_date : Optional[str] = None