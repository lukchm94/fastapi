from typing import Any, Dict, Optional

from fastapi import HTTPException


class NoDataException(HTTPException):
    def __init__(
        self,
        todo_id: int,
        status_code: Optional[int] = 404,
        detail: Optional[str] = "TODO with id {todo_id} not found",
        headers: Dict[str, Any] | None = None,
    ) -> None:
        super().__init__(status_code, detail.format(todo_id=todo_id), headers)


class MissingUserException(HTTPException):
    def __init__(
        self,
        username: str,
        status_code: Optional[int] = 401,
        detail: Optional[str] = "User: {username} not found",
        headers: Dict[str, Any] | None = None,
    ) -> None:
        super().__init__(status_code, detail.format(username=username), headers)


class FailedAuthenticationException(HTTPException):
    def __init__(
        self,
        status_code: Optional[int] = 401,
        detail: Optional[str] = "Authentication failed. Wrong password provided",
        headers: Dict[str, Any] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
