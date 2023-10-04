from model import Users
from models.users import UserRequest
from passlib.context import CryptContext

from fastapi import APIRouter, status

router = APIRouter()

bcrypt_context = CryptContext(schemas=["bcrypt"], deprecated="auto")


@router.get("/auth/")
async def get_users():
    return {"user": "authenticated"}


@router.post("/auth/", status_code=status.HTTP_201_CREATED)
async def create_user(user_request: UserRequest):
    create_user_model = Users(
        email=user_request.email,
        username=user_request.username,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        role=user_request.role,
        hashed_password=bcrypt_context(user_request.password),
        is_active=True,
    )
    return {"data": create_user_model}
