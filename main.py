from fastapi import FastAPI,HTTPException,Depends
from sqlalchemy.orm import Session
import models,schemas
from database import get_db
from routers import books,students,issued_book,login


app = FastAPI()

app.include_router(books.router) 
app.include_router(students.router)
app.include_router(issued_book.router)
app.include_router(login.router)

@app.get("/")
def get_root():
    return {
        "message":"Server is running fine...."
    }



