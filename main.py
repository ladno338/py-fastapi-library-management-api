from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, query

import schemas
import crud
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> query:
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)) -> query:
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)) -> query:
    db_author = crud.get_author_by_name(db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author already registered")
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> query:
    books = crud.get_books(db, skip=skip, limit=limit)
    return books


@app.post("/books/", response_model=schemas.Book)
def create_book_for_author(
    author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
) -> query:
    return crud.create_book(db=db, book=book, author_id=author_id)
