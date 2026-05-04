from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from infrastructure.postgres.repositories.base import BaseRepository
from infrastructure.postgres.models.comments import Comment
from core.exceptions.database_exceptions import CommentNotFoundException

class CommentRepository(BaseRepository[Comment]):
    def __init__(self):
        super().__init__(Comment, CommentNotFoundException)

    async def get_by_id_with_relations(
        self, session: AsyncSession, comment_id: int
    ) -> Comment | None:
        query = await session.execute(
            select(self._model)
            .options(
                joinedload(self._model.author),
                joinedload(self._model.post),
            )
            .where(self._model.id == comment_id)
        )
        comment = query.scalar()
        if not comment:
            raise CommentNotFoundException()
        return query.scalar()