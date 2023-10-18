from datetime import datetime, timedelta
from typing import Annotated

from database import SessionLocal
from exceptions import FailedAuthenticationException, MissingUserException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from model import Users
from models.token import Token
from models.users import UserRequest
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, status

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "ef91e4f65d4b1b011d0393d4ee2a33e62def383d4a8882e8f04a3e064dff6935"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DB_DEPENDENCY = Annotated[Session, Depends(get_db)]


@router.get("/")
async def get_users(db: DB_DEPENDENCY):
    data = db.query(Users).all()
    return {"users": len(data), "data": data}


@router.post("/", status_code=status.HTTP_201_CREATED)
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


@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DB_DEPENDENCY
):
    user = _authenticate_user(
        db=db, username=form_data.username, password=form_data.password
    )
    if user is not None:
        token = _create_access_token(
            username=user.username,
            user_id=user.id,
            role=user.role,
            expires_delta=timedelta(minutes=20),
        )
        return {"access_token": token, "token_type": "bearer"}
        # In order to implement the model below update models.Token
        return {"user": user, "token": {"access_token": token, "token_type": "bearer"}}


def _authenticate_user(db: DB_DEPENDENCY, username: str, password: str):
    user = db.query(Users).filter(Users.username == username).first()
    if user is None:
        raise MissingUserException(username=username)
    if not bcrypt_context.verify(password, user.hashed_password):
        raise FailedAuthenticationException()
    return user


def _create_access_token(
    username: str, user_id: int, role: str, expires_delta: timedelta
):
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(claims=encode, key=SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")
        if username is None or user_id is None:
            raise MissingUserException(username=username)
        return {"username": username, "user_id": user_id, "user_role": user_role}
    except JWTError:
        raise FailedAuthenticationException()
