from typing import Annotated

from database import SessionLocal
from exceptions import FailedAuthenticationException, NoDataException
from model import Todos
from models.todos import TodoRequest
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, Path, status

from .auth import get_current_user

router = APIRouter(prefix="/todo", tags=["Todo"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DB_DEPENDENCY = Annotated[Session, Depends(get_db)]
USER_DEPENDENCY = Annotated[dict, Depends(get_current_user)]


@router.get("/get_all", status_code=status.HTTP_200_OK)
async def read_all(db: DB_DEPENDENCY, user: USER_DEPENDENCY):
    return db.query(Todos).filter(Todos.owner_id == user.get("user_id")).all()


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_by_id(db: DB_DEPENDENCY, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return {"data": todo_model}
    raise NoDataException(todo_id=todo_id)


@router.post("/create_todo", status_code=status.HTTP_201_CREATED)
async def create_todo(
    db: DB_DEPENDENCY, user: USER_DEPENDENCY, todo_request: TodoRequest
):
    if user is None:
        raise FailedAuthenticationException()
    todo_model = Todos(**todo_request.dict(), owner_id=user.get("user_id"))
    db.add(todo_model)
    db.commit()


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: DB_DEPENDENCY, todo_request: TodoRequest, todo_id: int = Path(gt=0)
):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise NoDataException(todo_id=todo_id)

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: DB_DEPENDENCY, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise NoDataException(todo_id=todo_id)

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
