from fastapi import Body, FastAPI

app = FastAPI()


BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
    {"title": "Title Six", "author": "Author Two", "category": "math"},
]


class MissingError(Exception):
    def __init__(self, key: str) -> None:
        super().__init__(f"During the call for {key} nothing was returned")


@app.get("/books")
async def first_api():
    return {"message": BOOKS}


@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return: list[str] = []
    for book in BOOKS:
        if book.get("category").casefold().lower() == category.casefold().lower():
            books_to_return.append(book)

    if len(books_to_return) > 0:
        return {"message": books_to_return}

    else:
        return {"message": f"no books from {category.casefold().upper()}"}


@app.get("/books/{dynamic_param}")
async def read_all_books(dynamic_param: str):
    for book in BOOKS:
        if book.get("title").lower() == dynamic_param.casefold():
            return {"message": book}
        else:
            return {"message": "book not found"}


@app.get("/books/by_author/{author}")
async def get_book_by_author(author: str) -> None:
    books_to_returned: list[dict] = []
    for book in BOOKS:
        if book.get("author").casefold().lower() == author.casefold().lower():
            print(book)
            books_to_returned.append(book)

    if len(books_to_returned) > 0:
        return {"message": books_to_returned}
    else:
        # return {"message": "book not found"}
        raise MissingError(key=author)


@app.get("/book/{title}")
async def get_book_by_title(title: str):
    print(title.casefold().lower())
    if title.casefold().lower() in [book["title"].lower() for book in BOOKS]:
        return {
            "message": [
                book
                for book in BOOKS
                if str(book["title"].lower()) == title.casefold().lower()
            ]
        }
    else:
        return {"message": "book not found"}


@app.post("/books/create_book")
async def create_book(new_book=Body()) -> None:
    # new_book = Body()
    # print(new_book)
    BOOKS.append(new_book)


@app.put("/books/update_book")
async def update_book(updated_book=Body()) -> None:
    print(updated_book)
    for book in range(len(BOOKS)):
        if BOOKS[book].get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[book] = updated_book


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for book in range(len(BOOKS)):
        if BOOKS[book].get("title").casefold() == book_title.casefold():
            BOOKS.pop(book)
            break
