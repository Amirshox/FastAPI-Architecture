import enum

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import AbstractModel


class TaskStatus(enum.Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Task(AbstractModel):
    __tablename__ = "tasks"

    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(Enum(TaskStatus), default=TaskStatus.NEW)

    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    assignee_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)

    created_by: Mapped["User"] = relationship(
        "User", foreign_keys=[created_by_id], backref="created_tasks", lazy="joined"
    )
    assignee: Mapped["User"] = relationship(
        "User", foreign_keys=[assignee_id], backref="assigned_tasks", lazy="joined"
    )


__all__ = (
    "Task",
    "TaskStatus",
)
