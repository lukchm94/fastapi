from typing import Any, Optional

from pydantic import BaseModel, Field, root_validator

from fastapi import HTTPException


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

    @root_validator(pre=True)
    def validate_passwords(cls, values: dict) -> dict:
        password: str = values.get("password")
        new_password: str = values.get("new_password")

        if password == new_password:
            raise PasswordUpdateException()

        return values


class PasswordUpdateException(HTTPException):
    def __init__(
        self,
        status_code: Optional[int] = 422,
        detail: Optional[str] = "New and old passwords are the same",
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
