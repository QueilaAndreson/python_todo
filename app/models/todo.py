from sqlalchemy import Boolean, Column, DateTime, Integer, String, func

from app.database import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False, nullable=False)
    priority = Column(String, nullable=True)  # e.g. "low", "medium", "high"
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
