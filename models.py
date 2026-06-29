from database import Base
from sqlalchemy import Column,Integer,String,VARCHAR,ForeignKey,DATE,Boolean
from sqlalchemy.orm import relationship

class Book(Base):
    __tablename__="books"

    book_id = Column(Integer,index=True,primary_key=True)
    title = Column(String(255),unique=True,nullable=False)
    author = Column(String(255))
    is_available = Column(Boolean,default=True)
    issued_books = relationship("Issued_book",back_populates="book")

class Student(Base):
    __tablename__ = "student_data"

    student_id = Column(Integer,primary_key=True,index=True)
    name = Column(VARCHAR(255))
    role = Column(VARCHAR(10))
    email = Column(VARCHAR(255),unique=True)
    phone_number = Column(VARCHAR(255),unique=True)
    password = Column(VARCHAR(255))
    issued_books = relationship("Issued_book",back_populates="student")

class Issued_book(Base):
    __tablename__="issued_book"

    issue_id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer,ForeignKey("books.book_id"))
    issue_date = Column(DATE)
    return_date = Column(DATE)
    student_id = Column(Integer,ForeignKey("student_data.student_id"))
    book = relationship("Book",back_populates = "issued_books")
    student = relationship("Student",back_populates="issued_books")


