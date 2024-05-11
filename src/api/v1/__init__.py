from fastapi import APIRouter

from src.api.v1.users import auth_router, user_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(user_router)
v1_router.include_router(auth_router)
