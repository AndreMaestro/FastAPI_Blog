from infrastructure.postgres.database import database
from infrastructure.postgres.repositories.posts import PostRepository
from core.exceptions.domain_exceptions import PostNotFoundByIdException, ForbiddenException
from core.exceptions.database_exceptions import PostNotFoundException
import logging

logger = logging.getLogger(__name__)


class DeletePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self,
                      post_id: int,
                      author_id: int,
                      current_user_id: int,
                      is_superuser: bool = False) -> bool:
        if author_id != current_user_id and not is_superuser:
            error = ForbiddenException()
            logger.error("Только автор поста и администратор может удалить его")
            raise error
        try:
            async with self._database.session() as session:
                await self._repo.delete(session=session, id=post_id)
        except PostNotFoundException:
            raise PostNotFoundByIdException(id=post_id)

        return True