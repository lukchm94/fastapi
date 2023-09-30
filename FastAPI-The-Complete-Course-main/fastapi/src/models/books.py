from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Book:
    def __init__(
        self,
        id: int,
        title: str,
        author: str,
        category: str,
        rating: int,
        year_published: int,
    ) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.category = category
        self.rating = rating
        self.year_published = year_published


class BookRequest(BaseModel):
    id: Optional[int] = Field(id="id created automatically on server")
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    category: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=11)
    year_published: int = Field(gt=1999, lt=datetime.now().year + 1)

    class Config:
        schema_extra = {
            "example": {
                "title": "New Book",
                "Author": "Author",
                "category": "Category of a book",
                "rating": 5,
                "year_published": 2023,
            }
        }


def get_new_id(books: list[Book]) -> int:
    id: int = 0
    for book in books:
        if book.id > id:
            id = book.id
    return id + 1


BOOKS = [
    Book(1, "Tennis", "Me", "IT", 10, 2023),
    Book(2, "Tennis 2", "You", "IT", 9, 2022),
    Book(3, "Tennis 3", "He", "IT", 8, 2022),
    Book(4, "Tennis 4", "He", "sport", 8, 2021),
    Book(5, "Tennis 5", "He", "sport", 8, 2001),
]
