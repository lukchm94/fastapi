# source fastapienv/bin/activate
from typing import Annotated

from database import SessionLocal, engine
from models import Base, Todos
from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DB_DEPENDENCY = Annotated[Session, Depends(get_db)]


@app.get("/todos")
async def read_all(db: DB_DEPENDENCY):
    return db.query(Todos).all()
