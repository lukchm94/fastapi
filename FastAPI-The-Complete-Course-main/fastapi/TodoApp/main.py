# source fastapienv/bin/activate
from typing import Annotated

from database import SessionLocal, engine
from exceptions import NoDataException
from model import Base, Todos
from models.todos import TodoRequest
from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, Path, status

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DB_DEPENDENCY = Annotated[Session, Depends(get_db)]


@app.get("/home", status_code=status.HTTP_200_OK)
async def read_all(db: DB_DEPENDENCY):
    return db.query(Todos).all()


@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_by_id(db: DB_DEPENDENCY, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return {"data": todo_model}
    raise NoDataException(todo_id=todo_id)


@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: DB_DEPENDENCY, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.dict())

    db.add(todo_model)
    db.commit()


@app.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
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


@app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: DB_DEPENDENCY, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise NoDataException(todo_id=todo_id)

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
