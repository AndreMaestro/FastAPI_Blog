from datetime import datetime

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comments import CommentRepository
from schemas.comments import CommentResponseSchema, CommentCreateSchema


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, dto: CommentCreateSchema) -> CommentResponseSchema:
        with self._database.session() as session:
            comment = self._repo.create(
                session=session,
                text=dto.text,
                author_id=dto.author_id,
                post_id=dto.post_id,
                created_at=datetime.now(),
            )
            session.flush()
            comment_with_relations = self._repo.get_by_id_with_relations(
                session=session, comment_id=comment.id
            )

        return CommentResponseSchema.model_validate(obj=comment_with_relations)