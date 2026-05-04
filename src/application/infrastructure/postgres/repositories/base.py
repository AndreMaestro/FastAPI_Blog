from typing import Type, TypeVar, Generic

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from infrastructure.postgres.database import Base

ModelType = TypeVar('ModelType', bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], not_found_exception: Type[Exception]):
        self._model = model
        self._not_found_exception = not_found_exception

    async def create(self, session: AsyncSession, **data) -> ModelType:
        query = insert(self._model).values(**data).returning(self._model)
        obj = await session.scalar(query)
        await session.flush()
        return obj

    async def get_by_id(self, session: AsyncSession, id: int) -> ModelType:
        query = select(self._model).where(self._model.id == id)
        obj = await session.scalar(query)
        if obj is None:
            raise self._not_found_exception(id)
        return obj

    async def get_all(
            self, session: AsyncSession, limit: int = 100, offset: int = 0
    ) -> list[ModelType]:
        query = await session.execute(
            select(self._model).limit(limit).offset(offset)
        )
        return list(query.scalars().all())

    async def update(self, session: AsyncSession, id: int, **data) -> ModelType:
        obj = await self.get_by_id(session, id)
        if obj is None:
            raise self._not_found_exception(id)
        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        await session.flush()
        return obj

    async def delete(self, session: AsyncSession, id: int) -> bool:
        obj = await self.get_by_id(session, id)
        await session.delete(obj)