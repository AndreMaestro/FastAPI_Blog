from infrastructure.postgres.database import database
from infrastructure.postgres.repositories.images import ImageRepository
from infrastructure.postgres.repositories.comments import CommentRepository
from core.exceptions.domain_exceptions import ForbiddenException, CommentNotFoundByIdException
import logging

from services.images import ImageService

logger = logging.getLogger(__name__)


class DeleteCommentImagesUseCase:
    def __init__(self):
        self._database = database
        self._comment_repo = CommentRepository()
        self._image_repo = ImageRepository()

    async def execute(self, comment_id: int,
                      current_user_id: int,
                      author_id: int,
                      is_superuser: bool = False) -> None:

        if author_id != current_user_id and not is_superuser:
            error = ForbiddenException()
            logger.error("Только автор может удалять картинки")
            raise error

        async with self._database.session() as session:
            comment =await self._comment_repo.get_by_id(session=session, id=comment_id)
            if not comment:
                raise CommentNotFoundByIdException(comment_id)

            images = await self._image_repo.get_images(session, "comment", comment_id)
            if images:
                images_paths = [img.file_path for img in images]
                self._image_repo.delete_images(session, "comment", comment_id)
                await ImageService.delete_images(images_paths)