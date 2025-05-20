from sqlalchemy import create_engine, text
from ..main import app
from ..routers.todos import get_db
from ..routers.auth import get_current_user
from fastapi import status

from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_authenticated(beforeEach):
    response = client.get("/api/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "title": "Test Todo",
            "description": "Test Description",
            "priority": 1,
            "complete": False,
            "owner_id": 1,
            "id": 1
        }
    ]

def test_read_one_authenticated(beforeEach):
    response = client.get("/api/todos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() =={
        "title": "Test Todo",
        "description": "Test Description",
        "priority": 1,
        "complete": False,
        "owner_id": 1,
        "id": 1
    }

def test_read_one_authenticated_not_found():
    response = client.get("/api/todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}  

def test_create_todo(beforeEach):
    response = client.post(
        "/api/todos",
        json={
            "title": "New Todo",
            "description": "New Description",
            "priority": 2,
            "complete": False,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    # assert response.json() == {
    #     "title": "New Todo",
    #     "description": "New Description",
    #     "priority": 2,
    #     "complete": False,
    #     "owner_id": 1,
    #     "id": 2
    # }

def test_update_todo(beforeEach):
    response = client.put(
        "/api/todos/1",
        json={
            "title": "Updated Todo",
            "description": "Updated Description",
            "priority": 3,
            "complete": True,
        },
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    updated_todo = client.get("/api/todos/1")
    assert updated_todo.json() == {
        "title": "Updated Todo",
        "description": "Updated Description",
        "priority": 3,
        "complete": True,
        "owner_id": 1,
        "id": 1
    }