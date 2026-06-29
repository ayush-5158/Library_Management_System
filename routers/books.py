from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from auth.jwt_handler import require_admin
import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/books",# @router.get('/') -> @router.get(/books)
    tags=["Books"]
)

@router.post("/add_book")
def add_book(books:list[schemas.BookCreate], db:Session = Depends(get_db),admin:models.Student = Depends(require_admin)):#since you are sending list of books so we need to mention list[schemas.Books]
    new_books=[]
    for book in books:
        existing_book = db.query(models.Book).filter(models.Book.title == book.title).first()
        
        if existing_book:
            continue

        new_book = models.Book(
            title=book.title,
            author=book.author,
        )

        new_books.append(new_book)
    
    db.add_all(new_books)
    db.commit()

    return{
        "message":f"{len(new_books)} books added succesfully",
    }

@router.get("/books")
def show_books(db:Session=Depends(get_db)):
    books = db.query(models.Book).all()
    return books


@router.get("/available")
def show_filter_book(db:Session=Depends(get_db)):
    books=db.query(models.Book).filter(
        models.Book.is_available=="True"
    ).all()
    return books

@router.patch("/update_book/{book_id}")
def update_book(book_id:int,book_updates:schemas.BookUpdate,db:Session=Depends(get_db)):
    book = db.query(models.Book).filter(
        models.Book.book_id == book_id
    ).first()

    if not book:
        raise HTTPException(status_code=404,detail="Book not found.")
    
    #convert python dict to json data
    updated_data = book_updates.model_dump(exclude_unset=True)

    for key,value in updated_data.items():
        setattr(book,key,value)

    db.commit()
    db.refresh(book)

    return book

@router.delete("/delete_book/{book_id}")
def delete_book(book_id:int,db : Session=Depends(get_db)):
    book = db.query(models.Book).filter(
        models.Book.book_id == book_id
    ).first()

    if not book:
        raise HTTPException(status_code=404,detail="Book not found.")
    
    db.delete(book)
    db.commit()
    
    return{
        "message": "Book Deleted Succesfully",
        "Book_name": book.title
    }