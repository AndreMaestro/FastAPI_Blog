from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from infrastructure.postgres.repositories.base import BaseRepository, ModelType
from infrastructure.postgres.models.categories import Category
from core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    CategorySlugAlreadyExistsException
)

class CategoryRepository(BaseRepository[Category]):
    def __init__(self):
        super().__init__(Category, CategoryNotFoundException)

    async def get_by_slug(self, session: AsyncSession, slug: str) -> Category:
        query = await session.execute(
            select(self._model).where(self._model.slug == slug)
        )
        category = query.scalar()
        if category is None:
            raise CategoryNotFoundException()
        return category

    async def create(self, session: AsyncSession, **data) -> Category:
        try:
            return await super().create(session=session, **data)
        except IntegrityError:
            raise CategorySlugAlreadyExistsException()