from infrastructure.postgres.database import database
from infrastructure.postgres.repositories.comments import CommentRepository
from core.exceptions.domain_exceptions import CommentNotFoundByIdException, ForbiddenException
from core.exceptions.database_exceptions import CommentNotFoundException
import logging

logger = logging.getLogger(__name__)


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self,
                      comment_id: int,
                      author_id: int,
                      current_user_id: int,
                      is_superuser: bool = False) -> bool:
        if author_id != current_user_id and not is_superuser:
            error = ForbiddenException()
            logger.error("Только автор комментария или администратор может удалить его")
            raise error
        async with self._database.session() as session:
            try:
                await self._repo.delete(session=session, id=comment_id)
            except CommentNotFoundException:
                raise CommentNotFoundByIdException(id=comment_id)

        return True