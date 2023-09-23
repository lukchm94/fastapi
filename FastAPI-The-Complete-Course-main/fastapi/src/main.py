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
async def create_book(new_book=Body()):
    # new_book = Body()
    print(new_book)
    BOOKS.append(new_book)
