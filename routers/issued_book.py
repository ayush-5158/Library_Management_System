from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session

import models,schemas
from database import get_db

router = APIRouter(
    prefix="/issue-book",
    tags=['Issue_book']
)

@router.post('/',response_model=schemas.IssuedBookResponse,status_code=status.HTTP_201_CREATED)
def issue_book(data:schemas.IssuedBook,db : Session=Depends(get_db)):

    student = db.query(models.Student).filter(models.Student.student_id == data.student_id).first()

    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Student not found.")
    
    #student mil gaya

    book = db.query(models.Book).filter(
        models.Book.book_id == data.book_id
    ).first() # Books table me jakr book_id se book dhundo

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found.")
    #book me book store hogaya jo book issue karna hai

    if not book.is_available:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"Book is currently not available.")
    
    #student exist karta hai, book bhi exist karta hai and book available bhi hai
    #step 1 : Add this issue entry to issued_book table

    #create pydantic model instance so that sql alchemy can load this info in table
    new_issue = models.Issued_book(
        book_id = book.book_id,
        issue_date = data.issue_date,
        student_id = student.student_id,
    )

    db.add(new_issue)
    book.is_available=False
    db.commit()
    db.refresh(new_issue)

    return new_issue

#book issue hogaya


#book return krna hai
@router.patch('/return',response_model=schemas.IssuedBookUpdate,status_code=status.HTTP_200_OK)
#data me issue_id hai and return date hai only
def return_book(data:schemas.IssuedBookUpdate,db:Session=Depends(get_db)):

    issue_data = db.query(models.Issued_book).filter(
        models.Issued_book.issue_id == data.issue_id
    ).first()
    #issue table se wo particular row mil gaya

    if not issue_data:
        raise HTTPException(status_code=404,detail="Issue Record not found")

    if issue_data.return_date :
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Book already returned.")
    #ab usse book id and details nikalenge
    # book = db.query(models.Book).filter(
    #     models.Book.book_id == issue_data.book_id
    # ).first()
    book = issue_data.book
    #yaha book store hogaya

    if not book:
        raise HTTPException(status_code=404,detail="Book not found")

    if book.is_available:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Book is not issued.")
    
    issue_data.return_date = data.return_date

    book.is_available = True
    db.commit()
    db.refresh(issue_data)

    return issue_data