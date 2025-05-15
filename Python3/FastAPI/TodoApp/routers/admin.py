from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path, status, APIRouter
from models import Todos
from database import SessionLocal, engine
from .auth import get_current_user

router = APIRouter(
     prefix="/api/v1/admin",
    tags=["admin"],
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(get_current_user)]

@router.get("/todo", status_code=status.HTTP_200_OK)
def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0) ):
    if not user or user.get:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    todo = db.query(Todos).all()
    if todo:
        return todo
    else:
        raise HTTPException(status_code=404, detail="Todo not found")
    