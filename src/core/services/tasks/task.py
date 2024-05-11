from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.services.base import AbstractBaseService, T
from src.db import get_async_session
from src.db.models.tasks import Task


class TaskService(AbstractBaseService[Task]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Task)

    async def create(self, user, **kwargs) -> T:
        kwargs["created_by_id"] = user.id
        return await super().create(**kwargs)


def get_task_service(session: AsyncSession = Depends(get_async_session)):
    return TaskService(session)
