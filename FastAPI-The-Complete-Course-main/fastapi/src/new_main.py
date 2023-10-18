from datetime import datetime

from exceptions import MissingBookError, RatingError, YearError
from models.books import BOOKS, Book, BookRequest, get_new_id
from starlette import status

from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/books", status_code=status.HTTP_200_OK)
async def get_all_books():
    return {"results": len(BOOKS), "message": BOOKS}


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0, lt=1000000)):
    for book in BOOKS:
        if book.id == book_id:
            return {"message": book}
    raise MissingBookError(book_id=book_id)


@app.get("/books/published_after/{year}", status_code=status.HTTP_200_OK)
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


@app.get("/books/published_before/{year}", status_code=status.HTTP_200_OK)
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


@app.put("/books/update_year_published/{year}", status_code=status.HTTP_204_NO_CONTENT)
async def updated_year_published(book: BookRequest):
    if book.year_published > datetime.now().year or book.year_published < 2000:
        raise YearError(year=book.year_published)

    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book


@app.get("/books/", status_code=status.HTTP_200_OK)
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


@app.post("/create_book/", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    book_request.id = get_new_id(books=BOOKS)
    new_book: Book = Book(**book_request.dict())
    BOOKS.append(new_book)


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed: bool = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise MissingBookError(book_id=book.id)


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0, lt=1000000)):
    book_changed: bool = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise MissingBookError(book_id=book_id)
