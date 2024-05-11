from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.services.base import AbstractBaseService
from src.db import get_async_session
from src.db.models.users import User


class UserService(AbstractBaseService[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def get_by_username(self, username: str) -> User:
        async with self.session:
            query = select(self.model).where(self.model.username.icontains(username))
            result = await self.session.execute(query)
            instance = result.scalars().first()
            return instance

    async def authenticate_user(self, username: str, password: str) -> User:
        user = await self.get_by_username(username)
        if not user:
            raise ValueError("User not found")
        if not user.verify_password(password):
            raise ValueError("Invalid password")
        return user

    async def create(self, **kwargs) -> User:
        username = kwargs.get("username")
        user = await self.get_by_username(username)
        if user:
            raise ValueError("Username already exists")

        password = kwargs.pop("password")

        instance = self.model(**kwargs)
        instance.set_password(password)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def update(self, id_: int, **kwargs) -> User:
        username = kwargs.get("username")
        user = await self.get_by_username(username)
        if user and user.id != id_:
            raise ValueError("Email already exists")
        return await super().get_and_update(id_, **kwargs)

    async def update_password(
        self, id_: int, old_password: str, new_password: str
    ) -> User:
        user = await self.get_by_id(id_)
        if not user:
            raise ValueError("User not found")
        if not user.verify_password(old_password):
            raise ValueError("Invalid password")
        user.set_password(new_password)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user


def get_user_service(session: AsyncSession = Depends(get_async_session)) -> UserService:
    return UserService(session)
