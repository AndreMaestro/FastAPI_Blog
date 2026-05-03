import logging

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comments import CommentRepository
from infrastructure.sqlite.repositories.images import ImageRepository
from services.images import ImageService
from core.exceptions.domain_exceptions import ForbiddenException, CommentNotFoundByIdException
from core.exceptions.database_exceptions import ImageNotFoundException

logger = logging.getLogger(__name__)


class DeleteCommentImageByIdUseCase:
    def __init__(self):
        self._database = database
        self._comment_repo = CommentRepository()
        self._image_repo = ImageRepository()

    async def execute(
            self,
            comment_id: int,
            image_id: int,
            current_user_id: int,
            author_id: int,
            is_superuser: bool = False
    ) -> None:
        if author_id != current_user_id and not is_superuser:
            error = ForbiddenException()
            logger.error("Только автор может удалять картинки")
            raise error

        with self._database.session() as session:
            comment = self._comment_repo.get_by_id(session, comment_id)
            if not comment:
                raise CommentNotFoundByIdException(comment_id)

            image = self._image_repo.get_by_id(session, image_id)
            if not image or image.object_id != comment_id or image.content_type != "comment":
                raise ImageNotFoundException(image_id)

            await ImageService.delete_image(image.file_path)

            session.delete(image)
            session.flush()