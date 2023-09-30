from datetime import datetime

from exceptions import RatingError, YearError
from models.books import BOOKS, Book, BookRequest, get_new_id

from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/books")
async def get_all_books():
    return {"results": len(BOOKS), "message": BOOKS}


@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int = Path(gt=0, lt=1000000)):
    for book in BOOKS:
        if book.id == book_id:
            return {"message": book}
    return {"message": f"No book found for ID: {book_id}"}


@app.get("/books/published_after/{year}")
async def get_book_published_after(
    year: int = Path(gt=2000, lt=datetime.now().year + 1)
):
    # if year > datetime.now().year or year < 2000:
    #     raise YearError(year=year)

    books_to_return: list[Book] = []
    for book in BOOKS:
        if book.year_published >= year:
            books_to_return.append(book)
    if len(books_to_return) > 0:
        return {"results": len(books_to_return), "data": books_to_return}
    else:
        return {"message": f"No book published after {year}"}


@app.get("/books/published_before/{year}")
async def get_book_published_before(
    year: int = Path(gt=2000, lt=datetime.now().year + 1)
):
    # if year > datetime.now().year or year < 2000:
    #     raise YearError(year=year)

    books_to_return: list[Book] = []
    for book in BOOKS:
        if book.year_published <= year:
            books_to_return.append(book)
    if len(books_to_return) > 0:
        return {"results": len(books_to_return), "data": books_to_return}
    else:
        return {"message": f"No book published after {year}"}


@app.put("/books/update_year_published/{year}")
async def updated_year_published(book: BookRequest):
    if book.year_published > datetime.now().year or book.year_published < 2000:
        raise YearError(year=book.year_published)

    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book


@app.get("/books/")
async def get_book_by_rating(rating: int = Query(gt=0, lt=11)):
    if rating > 10:
        raise RatingError(rating=rating)

    books_to_return: list[Book] = []
    for book in BOOKS:
        if book.rating > rating:
            books_to_return.append(book)
    if len(books_to_return) > 0:
        return {"message": books_to_return}
    else:
        return {"message": f"No book found with rating higher than {rating}"}


@app.post("/create_book/")
async def create_book(book_request: BookRequest):
    book_request.id = get_new_id(books=BOOKS)
    new_book: Book = Book(**book_request.dict())
    BOOKS.append(new_book)


@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book


@app.delete("/books/{book_id}")
async def delete_book(book_id: int = Path(gt=0, lt=1000000)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break
