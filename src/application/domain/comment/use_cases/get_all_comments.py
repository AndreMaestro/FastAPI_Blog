from typing import List

from infrastructure.postgres.database import database
from infrastructure.postgres.repositories.comments import CommentRepository
from schemas.comments import CommentResponseSchema


class GetAllCommentsUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, limit: int = 100, offset: int = 0) -> List[CommentResponseSchema]:
        async with self._database.session() as session:
            comments = await self._repo.get_all(session=session, limit=limit, offset=offset)

        return [
            CommentResponseSchema.model_validate(obj=comment)
            for comment in comments
        ]