# Todo API

A simple task management REST API built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**, containerized with **Docker**.

## Tech Stack
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- PostgreSQL (database)
- Pydantic (validation)
- Docker & docker-compose
- Pytest (testing)

## Features
- Full CRUD for todos (create, read, update, delete)
- Filtering by completion status
- Pagination (skip/limit)
- Request/response validation with Pydantic
- Auto-generated interactive API docs (Swagger UI)

## Getting Started

### Run with Docker (recommended)
```bash
docker-compose up --build
```
The API will be available at `http://localhost:8000`.
Interactive docs: `http://localhost:8000/docs`

### Run locally without Docker
```bash
pip install -r requirements.txt
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/todo_db
uvicorn app.main:app --reload
```

## Running Tests
```bash
pip install -r requirements.txt
pytest
```
Tests use an in-memory SQLite database, so no Postgres setup is needed to run them.

## API Endpoints

| Method | Endpoint         | Description                    |
|--------|------------------|---------------------------------|
| POST   | `/todos`         | Create a new todo               |
| GET    | `/todos`         | List todos (filter/paginate)    |
| GET    | `/todos/{id}`    | Get a single todo               |
| PUT    | `/todos/{id}`    | Update a todo                   |
| DELETE | `/todos/{id}`    | Delete a todo                   |

### Example Request
```bash
curl -X POST http://localhost:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn FastAPI", "priority": "high"}'
```

## Project Structure
```
todo-api/
├── app/
│   ├── main.py          # App entrypoint
│   ├── database.py      # DB connection/session
│   ├── models/          # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   └── routers/          # API route handlers
├── tests/                # Pytest test suite
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Roadmap
- [ ] Add authentication (JWT)
- [ ] Add an LLM-powered endpoint (e.g. auto-generate subtasks from a todo title using RAG)
- [ ] Add due-date reminders
