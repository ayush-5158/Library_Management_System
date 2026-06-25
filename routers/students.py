from fastapi import APIRouter,HTTPException,Depends,status
from sqlalchemy.orm import Session
from sqlalchemy import or_

import models,schemas
from database import get_db

router = APIRouter(
    prefix="/students",# @router.get('/') -> @router.get(/students)
    tags=["Students"]
)


@router.post("/add",response_model = schemas.StudentResponse,status_code=status.HTTP_201_CREATED)#added status code here since if post execute succesfully then it will create the data, so the http should respond 201 created instead of simple 200 ok
def add_students(student_data:schemas.Student,db:Session=Depends(get_db)):
    
    existing_student = db.query(models.Student).filter(or_(models.Student.email == student_data.email, models.Student.phone_number == student_data.phone_number)).first()

    if existing_student:
        if existing_student.email == student_data.email:
            raise HTTPException(status_code=409,detail="Email already in use.")
        
        if existing_student.phone_number == student_data.phone_number:
            raise HTTPException(status_code=409,detail="Phone number already in use.")
    
    new_student = models.Student(
        name = student_data.name,
        email = student_data.email,
        grade = student_data.grade,
        phone_number = student_data.phone_number,
        password = student_data.password
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

@router.post("/add-bulk",response_model = list[schemas.StudentResponse],status_code=status.HTTP_201_CREATED)
def add_student_bulk(students_data:list[schemas.Student],db:Session=Depends(get_db)):

    new_students=[]

    for student in students_data:
        existing_student = db.query(models.Student).filter(or_(models.Student.email == student.email, models.Student.phone_number == student.phone_number)).first()

        if existing_student:
            continue

        new_student = models.Student(
            name = student.name,
            email = student.email,
            grade = student.grade,
            phone_number = student.phone_number,
            password = student.password
        )

        new_students.append(new_student)

    db.add_all(new_students)
    db.commit()

    for student in new_students:
        db.refresh(student)

    return new_students

@router.get("/all",response_model=list[schemas.StudentResponse],status_code=status.HTTP_200_OK) #added list[] as response will give list of students
def all_students(db:Session=Depends(get_db)):
    students = db.query(models.Student).all()
    return students

@router.get("/{student_id}",response_model=schemas.StudentResponse,status_code=200)
def get_student(student_id:int,db:Session=Depends(get_db)):
    student = db.query(models.Student).filter(
        models.Student.student_id == student_id
    ).first()

    if not student:
        raise HTTPException(status_code=404,detail="Student not found.")
    
    return student

@router.patch("/update/{student_id}",response_model=schemas.StudentResponse)
def update_student(student_id:int,updates:schemas.StudentUpdate,db:Session=Depends(get_db)):
    student = db.query(models.Student).filter(
        models.Student.student_id == student_id
    ).first()

    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Student with student_Id - {student_id} not exists. ")
    
    #convert updated_data python instance to json file
    updated_data = updates.model_dump(exclude_unset=True)

    for key,value in updated_data.items():
        setattr(student,key,value)

    db.commit()
    db.refresh(student)

    return student


@router.delete("/delete/{student_id}",response_model=schemas.StudentResponse)
def delete_student(student_id:int,db:Session=Depends(get_db)):
    student = db.query(models.Student).filter(
        models.Student.student_id == student_id
    ).first()

    if not student:
        raise HTTPException(status_code=404,detail="Student not found.")

    db.delete(student)
    db.commit()
    
    return student

