from fastapi import APIRouter, Depends, HTTPException, status

from src.core.schemas.tasks import (
    TaskCreateSchema,
    TaskDetailSchema,
    TaskListSchema,
    TaskUpdateSchema,
)
from src.core.services.tasks import get_task_service
from src.core.services.users.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskListSchema], status_code=status.HTTP_200_OK)
async def get_tasks(
    limit: int = 25,
    offset: int = 0,
    task_service=Depends(get_task_service),
    current_user=Depends(get_current_user),
):
    tasks = await task_service.get_all(limit, offset)
    return tasks


@router.post("", response_model=TaskDetailSchema, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreateSchema,
    task_service=Depends(get_task_service),
    current_user=Depends(get_current_user),
):
    task = await task_service.create(user=current_user, **task_data.dict())
    return task


@router.get("/{pk}", response_model=TaskDetailSchema, status_code=status.HTTP_200_OK)
async def get_task(
    pk: int,
    task_service=Depends(get_task_service),
    current_user=Depends(get_current_user),
):
    try:
        return await task_service.get_by_id(pk)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.put(
    "/{task_id}", response_model=TaskDetailSchema, status_code=status.HTTP_200_OK
)
async def update_task(
    pk: int,
    task_data: TaskUpdateSchema,
    task_service=Depends(get_task_service),
    current_user=Depends(get_current_user),
):
    task = await task_service.update(pk, **task_data.dict())
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.delete("/{pk}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    pk: int,
    task_service=Depends(get_task_service),
    current_user=Depends(get_current_user),
):
    try:
        await task_service.get_and_delete(pk)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    return None
