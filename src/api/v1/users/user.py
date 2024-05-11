from fastapi import APIRouter, Depends, HTTPException, status

from src.core.schemas.users import (
    UserCreateSchema,
    UserDetailSchema,
    UserListSchema,
    UserUpdatePasswordSchema,
    UserUpdateSchema,
)
from src.core.services.users import get_current_user, get_user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserDetailSchema, status_code=status.HTTP_200_OK)
async def get_me(
    current_user=Depends(get_current_user),
):
    return current_user


@router.put("/me", response_model=UserDetailSchema, status_code=status.HTTP_200_OK)
async def update_me(
    user_data: UserUpdateSchema,
    current_user=Depends(get_current_user),
    user_service=Depends(get_user_service),
):
    try:
        user = await user_service.update(current_user.id, **user_data.dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    return user


@router.post("/me/update-password", status_code=status.HTTP_200_OK)
async def update_password(
    user_data: UserUpdatePasswordSchema,
    current_user=Depends(get_current_user),
    user_service=Depends(get_user_service),
):
    try:
        await user_service.update_password(
            current_user.id, user_data.old_password, user_data.new_password
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return {"message": "Password updated successfully"}


@router.get("", response_model=list[UserListSchema], status_code=status.HTTP_200_OK)
async def get_users(
    limit: int = 25,
    offset: int = 0,
    user_service=Depends(get_user_service),
):
    users = await user_service.get_all(limit, offset)
    return users


@router.get("/{pk}", response_model=UserDetailSchema, status_code=status.HTTP_200_OK)
async def get_user(
    pk: int,
    user_service=Depends(get_user_service),
):
    try:
        user = await user_service.get_by_id(pk)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    return user


@router.post("", response_model=UserDetailSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreateSchema,
    user_service=Depends(get_user_service),
):
    try:
        user = await user_service.create(**user_data.dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return user


@router.put("/{pk}", response_model=UserDetailSchema, status_code=status.HTTP_200_OK)
async def update_user(
    pk: int,
    user_data: UserUpdateSchema,
    user_service=Depends(get_user_service),
):
    try:
        user = await user_service.update(pk, **user_data.dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    return user


@router.delete("/{pk}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    pk: int,
    user_service=Depends(get_user_service),
):
    try:
        await user_service.delete(pk)
        return {"message": "User deleted successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
