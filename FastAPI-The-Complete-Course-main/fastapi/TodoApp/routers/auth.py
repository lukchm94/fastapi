from typing import Annotated

from database import SessionLocal
from exceptions import FailedAuthenticationException, MissingUserException
from fastapi.security import OAuth2PasswordRequestForm
from model import Users
from models.users import UserRequest
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, status

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DB_DEPENDENCY = Annotated[Session, Depends(get_db)]


@router.get("/auth/")
async def get_users(db: DB_DEPENDENCY):
    data = db.query(Users).all()
    return {"users": len(data), "data": data}


@router.post("/auth/", status_code=status.HTTP_201_CREATED)
async def create_user(db: DB_DEPENDENCY, user_request: UserRequest):
    create_user_model = Users(
        email=user_request.email,
        username=user_request.username,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        role=user_request.role,
        hashed_password=bcrypt_context.hash(user_request.password),
        is_active=True,
    )

    db.add(create_user_model)
    db.commit()


@router.post("/token", status_code=status.HTTP_200_OK)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DB_DEPENDENCY
):
    user = _authenticate_user(
        db=db, username=form_data.username, password=form_data.password
    )
    if user is not None:
        return {"user": user}


def _authenticate_user(db: DB_DEPENDENCY, username: str, password: str):
    user = db.query(Users).filter(Users.username == username).first()
    if user is None:
        raise MissingUserException(username=username)
    if not bcrypt_context.verify(password, user.hashed_password):
        raise FailedAuthenticationException()
    return user
