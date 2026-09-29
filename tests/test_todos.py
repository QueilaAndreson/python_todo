import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

# Use an in-memory SQLite DB for fast, isolated tests
engine = create_engine(
    "sqlite:///:memory:", connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


def test_create_todo():
    response = client.post("/todos", json={"title": "Buy groceries"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["is_completed"] is False


def test_create_todo_missing_title():
    response = client.post("/todos", json={"description": "no title here"})
    assert response.status_code == 422


def test_list_todos():
    client.post("/todos", json={"title": "Task 1"})
    client.post("/todos", json={"title": "Task 2"})
    response = client.get("/todos")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_todo():
    created = client.post("/todos", json={"title": "Read a book"}).json()
    response = client.get(f"/todos/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Read a book"


def test_get_todo_not_found():
    response = client.get("/todos/999")
    assert response.status_code == 404


def test_update_todo():
    created = client.post("/todos", json={"title": "Old title"}).json()
    response = client.put(
        f"/todos/{created['id']}", json={"title": "New title", "is_completed": True}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New title"
    assert data["is_completed"] is True


def test_delete_todo():
    created = client.post("/todos", json={"title": "Delete me"}).json()
    response = client.delete(f"/todos/{created['id']}")
    assert response.status_code == 204
    get_response = client.get(f"/todos/{created['id']}")
    assert get_response.status_code == 404
