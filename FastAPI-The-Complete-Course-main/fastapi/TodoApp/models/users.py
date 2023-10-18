from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: str = Field(min_length=3, include="@")
    first_name: str = Field(min_length=3, max_length=100)
    last_name: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=3, max_length=100)
    role: str = Field(min_length=3, max_length=100)
