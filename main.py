from fastapi import FastAPI,HTTPException,status,Depends
from sqlalchemy.orm import Session
import models,schemas
from database import get_db


app = FastAPI()

@app.get("/")
def get_root():
    return {
        "message":"Server is running fine...."
    }

@app.post("/add_book")
def add_book(book:schemas.Books, db:Session = Depends(get_db)):

    existing_book = db.query(models.Books).filter(
        models.Books.title==book.title
    ).first()

    if existing_book:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Book Already Exists.")

    new_book = models.Books(title=book.title,author=book.author,is_available=book.is_available,assigned_to=book.assigned_to)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book

@app.get("/books")
def show_books(db:Session=Depends(get_db)):
    books = db.query(models.Books).all()
    return books


@app.get("/books/available")
def show_filter_book(db:Session=Depends(get_db)):
    books=db.query(models.Books).filter(
        models.Books.is_available=="Yes"
    ).all()

    return books

@app.patch("/update_book/{book_id}")
def update_book(book_id:int,book_updates:schemas.BookUpdate,db:Session=Depends(get_db)):
    book = db.query(models.Books).filter(
        models.Books.id == book_id
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

@app.delete("/delete_book/{book_id}")
def delete_book(book_id:int,db : Session=Depends(get_db)):
    book = db.query(models.Books).filter(
        models.Books.id == book_id
    ).first()

    if not book:
        raise HTTPException(status_code=404,detail="Book not found.")
    
    db.delete(book)
    db.commit()
    
    return{
        "message": "Book Deleted Succesfully",
        "Book_name": book.title
    }


