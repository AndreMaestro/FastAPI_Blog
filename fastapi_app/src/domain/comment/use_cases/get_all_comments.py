from typing import List

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comments import CommentRepository
from schemas.comments import CommentResponseSchema


class GetAllCommentsUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, limit: int = 100, offset: int = 0) -> List[CommentResponseSchema]:
        with self._database.session() as session:
            comments = self._repo.get_all(session=session, limit=limit, offset=offset)

        return [
            CommentResponseSchema.model_validate(obj=comment)
            for comment in comments
        ]