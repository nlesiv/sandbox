from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path, status
from .models import Base, Todos
from .database import SessionLocal, engine

from .routers import auth
from .routers import todos
from .routers import admin

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)


