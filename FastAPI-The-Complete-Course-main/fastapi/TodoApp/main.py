# source fastapienv/bin/activate

from database import engine
from model import Base
from routers import admin, auth, todos, users

from fastapi import FastAPI

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
