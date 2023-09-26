from models.books import BOOKS, Book, BookRequest

from fastapi import FastAPI

app = FastAPI()


@app.get("/books")
async def first_api():
    return {"message": BOOKS}


@app.post("/create_book/")
async def create_book(book_request: BookRequest):
    print(type(book_request))
    new_book: Book = Book(**book_request.dict())
    print(type(new_book))
    BOOKS.append(new_book)
