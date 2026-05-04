from sqlalchemy.orm import Session, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.util import await_only
from watchfiles import awatch

from infrastructure.postgres.repositories.base import BaseRepository
from infrastructure.postgres.models.posts import Post
from core.exceptions.database_exceptions import PostNotFoundException


class PostRepository(BaseRepository[Post]):
    def __init__(self):
        super().__init__(Post, PostNotFoundException)

    async def get_all(
        self, session: AsyncSession, limit: int = 100, offset: int = 0
    ) -> list[Post]:
        query = await session.execute(
            select(self._model)
            .options(
                joinedload(self._model.author),
                joinedload(self._model.category),
                joinedload(self._model.location),
            )
            .limit(limit)
            .offset(offset)
        )
        return list(query.scalars().all())

    async def get_by_id_with_relations(
        self, session: AsyncSession, post_id: int
    ) -> Post | None:
        query = await session.execute(
            select(self._model)
            .options(
                joinedload(self._model.author),
                joinedload(self._model.category),
                joinedload(self._model.location),
            )
            .where(self._model.id == post_id)
        )
        post = query.scalar()
        if post is None:
            raise PostNotFoundException()
        return post
