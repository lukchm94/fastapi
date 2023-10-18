# source fastapienv/bin/activate

from database import engine
from model import Base
from routers import auth, todos

from fastapi import FastAPI

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
