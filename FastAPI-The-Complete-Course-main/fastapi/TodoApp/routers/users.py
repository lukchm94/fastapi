from typing import Annotated

from database import SessionLocal
from exceptions import FailedAuthenticationException, NoDataException
from model import Users
from models.users import UserRequest
from models.verification import UserVerification
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, Path, status

from .auth import get_current_user

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(prefix="/user", tags=["user"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DB_DEPENDENCY = Annotated[Session, Depends(get_db)]
USER_DEPENDENCY = Annotated[dict, Depends(get_current_user)]


@router.get("/get_user", status_code=status.HTTP_200_OK)
async def read_all(user: USER_DEPENDENCY, db: DB_DEPENDENCY):
    if user is None:
        raise FailedAuthenticationException()
    res = db.query(Users).filter(Users.id == user.get("user_id")).first()

    return res


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: USER_DEPENDENCY, db: DB_DEPENDENCY, user_ver: UserVerification
):
    if user is None:
        raise FailedAuthenticationException()

    user_model = db.query(Users).filter(Users.id == user.get("user_id")).first()
    if not bcrypt_context.verify(user_ver.password, user_model.hashed_password):
        raise FailedAuthenticationException()

    user_model.hashed_password = bcrypt_context.hash(user_ver.new_password)
    db.add(user_model)
    db.commit()


@router.put("/update_user", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(user: USER_DEPENDENCY, db: DB_DEPENDENCY, user_req: UserRequest):
    if user is None:
        raise FailedAuthenticationException()

    user_to_update = db.query(Users).filter(Users.id == user.get("user_id")).first()
    # TODO finish the updates for the user
    user_to_update.hashed_password = bcrypt_context.hash(user_req.password)
    db.add(user_to_update)
    db.commit()


@router.delete("/delete_user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: USER_DEPENDENCY, db: DB_DEPENDENCY, user_id: int = Path(gt=0)
):
    if user is None:
        raise FailedAuthenticationException()

    user_model = db.query(Users).filter(Users.id == user_id).first()

    if user_model is None:
        raise NoDataException()

    db.query(Users).filter(Users.id == user_id).delete()
    db.commit()
