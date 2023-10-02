from typing import Any, Dict

from fastapi import HTTPException


class NoDataException(HTTPException):
    def __init__(
        self,
        todo_id: int,
        status_code: int = 404,
        detail: str = "TODO with id {todo_id} not found",
        headers: Dict[str, Any] | None = None,
    ) -> None:
        super().__init__(status_code, detail.format(todo_id=todo_id), headers)
