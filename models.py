from database import Base
from sqlalchemy import Column,Integer,String,VARCHAR

class Books(Base):
    __tablename__="books"

    book_id = Column(Integer,index=True,primary_key=True)
    title = Column(String(255),unique=True)
    author = Column(String(255))
    is_available = Column(String(255))
    assigned_to = Column(String(255))

class Student(Base):
    __tablename__ = "student_data"

    student_id = Column(Integer,primary_key=True,index=True)
    name = Column(VARCHAR(255))
    grade = Column(VARCHAR(10))
    email = Column(VARCHAR(255),unique=True)
    phone_number = Column(VARCHAR(255),unique=True)
    password = Column(VARCHAR(255))

class Issued_book(Base):
    __tablename__="issued_book"

    issue_id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer)
    issue_date = Column(VARCHAR(255))
    return_date = Column(VARCHAR(255))
    student_id = Column(Integer)

class Complaint(Base):
    __tablename__ = "complaints"

    complaint_id = Column(Integer,primary_key=True,index=True)
    student_id = Column(Integer)
    complaint = Column(VARCHAR(1000))
    complaint_date = Column(VARCHAR(255))
    resolved_date = Column(VARCHAR(255))
