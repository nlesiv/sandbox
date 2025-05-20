from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path, status, APIRouter
from ..models import Todos
from ..database import SessionLocal, engine
from .auth import get_current_user

router = APIRouter(
    prefix="/api/todos",
    tags=["todos"]
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(..., min_length=3)
    description: str = Field(..., min_length=3, max_length=100)
    priority: int = Field(..., gt=0, le=5)
    complete: bool = False

@router.get("/", status_code=status.HTTP_200_OK)
def read_all(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    todos = db.query(Todos).filter(Todos.owner_id == user.get('id')).all()
    return todos

@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0) ):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).first()
    if todo:
        return todo
    else:
        raise HTTPException(status_code=404, detail="Todo not found")
    
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_todo(user: user_dependency, db: db_dependency, todo: TodoRequest):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    todo_model = Todos(**todo.model_dump(), owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model

@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_todo(user: user_dependency, db: db_dependency, todo: TodoRequest, todo_id: int = Path(gt=0), ):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).first()
    if todo_model:
        for key, value in todo.model_dump().items():
            setattr(todo_model, key, value)
        db.add(todo_model)
        db.commit()
        db.refresh(todo_model)
        return todo_model
    else:
        raise HTTPException(status_code=404, detail="Todo not found")
    
@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model:
        db.delete(todo_model)
        db.commit()
        return
    else:
        raise HTTPException(status_code=404, detail="Todo not found")