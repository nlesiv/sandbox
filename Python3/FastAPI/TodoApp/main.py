from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path, status
import models
from database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    title: str = Field(..., min_length=3)
    description: str = Field(..., min_length=3, max_length=100)
    priority: int = Field(..., gt=0, le=5)
    completed: bool = False

@app.get("/", status_code=status.HTTP_200_OK)
def read_all(db: db_dependency):
    todos = db.query(models.Todos).all()
    return todos

@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
def read_todo(db: db_dependency, todo_id: int = Path(gt=0) ):
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo:
        return todo
    else:
        raise HTTPException(status_code=404, detail="Todo not found")
    
@app.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(db: db_dependency, todo: TodoRequest):
    todo_model = models.Todos(**todo.model_dump())
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model

@app.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_todo(db: db_dependency, todo: TodoRequest, todo_id: int = Path(gt=0), ):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo_model:
        for key, value in todo.model_dump().items():
            setattr(todo_model, key, value)
        db.add(todo_model)
        db.commit()
        db.refresh(todo_model)
        return todo_model
    else:
        raise HTTPException(status_code=404, detail="Todo not found")
    
@app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo_model:
        db.delete(todo_model)
        db.commit()
        return
    else:
        raise HTTPException(status_code=404, detail="Todo not found")