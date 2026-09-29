from fastapi import FastAPI

from app.database import Base, engine
from app.routers import todos

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo API",
    description="A simple task management API built with FastAPI, SQLAlchemy, and PostgreSQL.",
    version="1.0.0",
)

app.include_router(todos.router)


@app.get("/")
def root():
    return {"message": "Todo API is running. Visit /docs for API documentation."}


@app.get("/health")
def health_check():
    return {"status": "ok"}
