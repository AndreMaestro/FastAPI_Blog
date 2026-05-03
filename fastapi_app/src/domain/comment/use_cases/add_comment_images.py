from typing import List

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comments import CommentRepository
from infrastructure.sqlite.repositories.images import ImageRepository
from schemas.comments import CommentResponseSchema
from core.exceptions.domain_exceptions import ForbiddenException, CommentNotFoundByIdException
from fastapi import UploadFile
import logging

from services.images import ImageService

logger = logging.getLogger(__name__)


class AddCommentImagesUseCase:
    def __init__(self):
        self._database = database
        self._comment_repo = CommentRepository()
        self._image_repo = ImageRepository()

    async def execute(self, comment_id: int,
                      images: List[UploadFile],
                      current_user_id: int,
                      author_id: int) -> CommentResponseSchema:

        if author_id != current_user_id:
            error = ForbiddenException()
            logger.error("Только автор может добавлять картинки к комментариям")
            raise error
        with self._database.session() as session:
            comment = self._comment_repo.get_by_id(session=session, id=comment_id)
            if not comment:
                raise CommentNotFoundByIdException(comment_id)

            if images:
                image_paths = await ImageService.save_images(images, "comment", comment_id)
                self._image_repo.add_images(session, "comment", comment_id, image_paths)

            session.flush()
        return CommentResponseSchema.model_validate(obj=comment)