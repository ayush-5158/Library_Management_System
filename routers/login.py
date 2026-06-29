from fastapi import APIRouter,HTTPException,Depends,status
from sqlalchemy.orm import Session
from auth.hashing import verify_password
from auth.jwt_handler import create_access_token,get_current_user,require_admin
from fastapi.security import OAuth2PasswordRequestForm

import models,schemas
from database import get_db

router = APIRouter()

@router.post("/login")
def login(form_data:OAuth2PasswordRequestForm= Depends(),db:Session=Depends(get_db)):
    #find user
    user = db.query(models.Student).filter(
        models.Student.email==form_data.username
    ).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials.")
    
    #user found
    #password checking
    #hash password, plain password
    verifying_password = verify_password(form_data.password,user.password)

    if not verifying_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials.")

    token = create_access_token({
        "student_id" : user.student_id,
        "role" : user.role
    })

    return {
        "access_token":token,
        "token_type": "bearer"
    }

    
@router.get("/profile")
def profile(current_user : models.Student = Depends(get_current_user),db:Session=Depends(get_db)):

    return{
        "message":f"Hello {current_user.name} and you have issued {len(current_user.issued_books)} book"
    }

@router.get("/admin/dashboard")
def dashboard(admin:models.Student = Depends(require_admin), db:Session=Depends(get_db)):
    total_books = db.query(models.Book).count()
    available_books = db.query(models.Book).filter(models.Book.is_available==True).count()
    issued_books = db.query(models.Issued_book).filter(models.Issued_book.return_date==None).count()
    total_students = db.query(models.Student).filter(models.Student.role=='student').count()

    return{
        "total_books" : total_books,
        "available_books" : available_books,
        "issued_books" : issued_books,
        "total_students" : total_students
    }
