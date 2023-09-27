from models.books import BOOKS, Book, BookRequest, get_new_id

from fastapi import FastAPI

app = FastAPI()


@app.get("/books")
async def first_api():
    return {"message": BOOKS}


@app.post("/create_book/")
async def create_book(book_request: BookRequest):
    book_request.id = get_new_id(books=BOOKS)
    new_book: Book = Book(**book_request.dict())
    BOOKS.append(new_book)
