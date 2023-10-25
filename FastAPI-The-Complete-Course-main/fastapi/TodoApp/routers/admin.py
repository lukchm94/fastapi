from typing import Annotated

from database import SessionLocal
from exceptions import FailedAuthenticationException, NoDataException
from model import Todos
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, Path, status

from .auth import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DB_DEPENDENCY = Annotated[Session, Depends(get_db)]
USER_DEPENDENCY = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: USER_DEPENDENCY, db: DB_DEPENDENCY):
    if user is None or user.get("user_role") != "admin":
        raise FailedAuthenticationException()
    res = db.query(Todos).all()
    return {"elements": len(res), "data": res}


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: USER_DEPENDENCY, db: DB_DEPENDENCY, todo_id: int = Path(gt=0)
):
    if user is None or user.get("user_role") != "admin":
        raise FailedAuthenticationException()

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is None:
        raise NoDataException()

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
