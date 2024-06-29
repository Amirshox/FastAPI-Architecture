from abc import ABC
from typing import Any, Generic, Sequence, Tuple, Type, TypeVar

from fastapi import HTTPException
from sqlalchemy import Row, delete, func, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.logger import logger

# Define a generic variable for your model
T = TypeVar("T")


class AbstractBaseService(ABC, Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def create(self, **kwargs) -> T:
        try:
            instance = self.model(**kwargs)
            self.session.add(instance)
            await self.session.commit()
            await self.session.refresh(instance)
            return instance
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=400, detail="Relationship with specified ID does not exist"
            )

    async def update(self, id_: int, **kwargs) -> None:
        async with self.session:
            update(self.model).where(self.model.id == id_).values(**kwargs)
            await self.session.commit()

    async def get_and_update(self, id_: int, **kwargs) -> T:
        async with self.session:
            instance = await self.get_by_id(id_)
            for key, value in kwargs.items():
                setattr(instance, key, value)
            self.session.add(instance)
            await self.session.commit()
            await self.session.refresh(instance)
            return instance

    async def delete(self, id_: int) -> None:
        async with self.session:
            delete(self.model).where(self.model.id == id_)
            await self.session.commit()

    async def get_and_delete(self, id_: int) -> None:
        async with self.session:
            instance = await self.get_by_id(id_)
            await self.session.delete(instance)
            await self.session.commit()

    async def get_by_id(self, id_: int) -> T:
        async with self.session:
            query = select(self.model).where(self.model.id == id_)
            result = await self.session.execute(query)
            instance = result.scalars().first()
            if not instance:
                raise ValueError(f"{self.model.__name__} not found")
            return instance

    async def get_all(
        self,
        limit: int = 25,
        offset: int = 0,
    ) -> Sequence[Row[Any]]:
        query = select(self.model)

        query = query.limit(limit).offset(offset)

        async with self.session as session:
            try:
                result = await session.execute(query)
            except SQLAlchemyError as e:
                logger.error(f"Error executing query: {e}")
                return []

            instances = result.scalars().all()
        return instances

    async def get_all_paginated(
        self,
        page: int = 1,
        page_size: int = 25,
    ) -> Tuple[int, Sequence[Row[Any]]]:
        limit = page_size
        offset = (page - 1) * page_size

        instances = await self.get_all(
            limit=limit,
            offset=offset,
        )
        count = await self.get_count()
        return count, instances

    async def get_count(
        self,
    ) -> int:
        query = select(func.count()).select_from(self.model)

        # get count
        async with self.session as session:
            try:
                result = await session.execute(query)
            except SQLAlchemyError as e:
                logger.error(f"Error executing query: {e}")
                return 0

            count = result.scalar()
        return count
