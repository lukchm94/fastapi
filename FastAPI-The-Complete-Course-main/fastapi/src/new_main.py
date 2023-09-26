from models.books import BOOKS

from fastapi import Body, FastAPI

app = FastAPI()


@app.get("/books")
async def first_api():
    return {"message": BOOKS}


@app.post("/books/create_book/")
async def create_book(new_book=Body()):
    # new_book.get("id") =
    return BOOKS.append(new_book)
