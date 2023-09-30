from datetime import datetime
from typing import Any, Dict

from fastapi import HTTPException


# TODO replace Exception with HTTPException
class RatingError(Exception):
    def __init__(self, rating: int) -> None:
        super().__init__(f"Rating of {rating} not allowed. Max rating is 10")


class YearError(Exception):
    def __init__(self, year: int) -> None:
        super().__init__(
            f"{year} not allowed choose year between 2000 and {datetime.now().year}"
        )


class MissingBookError(HTTPException):
    def __init__(
        self,
        book_id: int,
        status_code: int = 404,
        detail: str = "Book with ID: {id} not found",
        headers: Dict[str, Any] | None = None,
    ) -> None:
        super().__init__(status_code, detail.format(id=book_id), headers)
