import enum

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import AbstractModel


class TaskStatus(enum.Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Task(AbstractModel):
    __tablename__ = "tasks__task"

    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(Enum(TaskStatus), default=TaskStatus.NEW)

    author_id: Mapped[int] = mapped_column(nullable=False)
    assignee_id: Mapped[int] = mapped_column(nullable=False)

    author = relationship("User", back_populates="tasks")
    assignee = relationship("User", back_populates="assigned_tasks")


__all__ = (
    "Task",
    "TaskStatus",
)
