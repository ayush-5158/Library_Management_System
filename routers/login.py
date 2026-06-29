from fastapi import APIRouter,HTTPException,Depends,status
from sqlalchemy.orm import Session
from auth.hashing import verify_password
from auth.jwt_handler import create_access_token,get_current_user
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
        "grade" : user.grade
    })

    return {
        "access_token":token,
        "token_type": "bearer"
    }

    
@router.get("/profile")
def profile(current_user : models.Student = Depends(get_current_user),db:Session=Depends(get_db)):

    return{
        "message":f"Hello {current_user.name}"
    }