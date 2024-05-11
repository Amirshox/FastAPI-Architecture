from enum import Enum

from pydantic import BaseModel

from src.db.models.tasks import TaskStatus


class TaskBaseSchema(BaseModel):
    title: str
    description: str
    status: TaskStatus
    assignee_id: int | None


class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskUpdateSchema(TaskBaseSchema):
    pass


class TaskListSchema(TaskBaseSchema):
    id: int


class TaskDetailSchema(TaskBaseSchema):
    id: int
