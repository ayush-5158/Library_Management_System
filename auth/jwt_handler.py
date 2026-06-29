from jose import jwt,JWTError
from datetime import UTC,datetime,timedelta
from fastapi import HTTPException,Depends
from sqlalchemy.orm import Session
from database import get_db
from fastapi.security import OAuth2PasswordBearer
import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login") # we are using this just to extract jwt, if we dont want to use it we can simply do token.split('')[1] or token.replace("Bearer","")

SECRET_KEY ="Ayush@1927@LibraryBackendProject"
EXPIRE_TIME = 30
SIGNING_ALGORITHM ='HS256'


def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(UTC)+timedelta(minutes=EXPIRE_TIME)
    to_encode.update({'exp':expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=SIGNING_ALGORITHM)


def verify_access_token(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[SIGNING_ALGORITHM])
        return payload
    
    except JWTError:
        raise HTTPException(status_code=401,detail="Credentials are not verified.",headers={"WWW-Authenticate":"Bearer"})

 
def get_current_user(token:str=Depends(oauth2_scheme),db:Session = Depends(get_db))->models.Student:
    payload = verify_access_token(token)

    #verification of token done now querying db

    current_user = db.query(models.Student).filter(models.Student.student_id == payload.get('student_id')).first()
    if current_user is None:
        #user got deleted
        raise HTTPException(status_code=401,detail='Could not validate credentials.')
    return current_user
    