from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comments import CommentRepository
from schemas.comments import CommentResponseSchema


class GetCommentByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> CommentResponseSchema:
        with self._database.session() as session:
            comment = self._repo.get_by_id_with_relations(session=session, comment_id=comment_id)

        if comment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Comment with id {comment_id} not found',
            )

        return CommentResponseSchema.model_validate(obj=comment)