from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comments import CommentRepository
from schemas.comments import CommentUpdateSchema, CommentResponseSchema
from core.exceptions.domain_exceptions import CommentNotFoundByIdException, ForbiddenException
from core.exceptions.database_exceptions import CommentNotFoundException
import logging

logger = logging.getLogger(__name__)


class UpdateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self,
                      comment_id: int,
                      dto: CommentUpdateSchema,
                      author_id: int,
                      current_user_id: int) -> CommentResponseSchema:
        if author_id != current_user_id:
            error = ForbiddenException()
            logger.error("Только автор комментария может обновлять его")
            raise error

        with self._database.session() as session:
            try:
                comment = self._repo.update(
                    session=session,
                    id=comment_id,
                    text=dto.text,
                )
                comment_with_relations = self._repo.get_by_id_with_relations(
                    session=session, comment_id=comment.id
                )
            except CommentNotFoundException:
                raise CommentNotFoundByIdException(id=comment_id)

        return CommentResponseSchema.model_validate(obj=comment_with_relations)