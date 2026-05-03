from typing import List

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.images import ImageRepository
from infrastructure.sqlite.repositories.posts import PostRepository
from schemas.posts import PostResponseSchema
from core.exceptions.domain_exceptions import ForbiddenException, PostNotFoundByIdException
from fastapi import UploadFile
import logging

from services.images import ImageService

logger = logging.getLogger(__name__)


class AddPostImagesUseCase:
    def __init__(self):
        self._database = database
        self._post_repo = PostRepository()
        self._image_repo = ImageRepository()

    async def execute(self, post_id: int,
                      images: List[UploadFile],
                      current_user_id: int,
                      author_id: int) -> PostResponseSchema:

        if author_id != current_user_id:
            error = ForbiddenException()
            logger.error("Только автор может добавлять картинки к постам")
            raise error
        with self._database.session() as session:
            post = self._post_repo.get_by_id(session=session, id=post_id)
            if not post:
                raise PostNotFoundByIdException(post_id)
            if images:
                image_paths = await ImageService.save_images(images, "post", post_id)
                self._image_repo.add_images(session, "post", post_id, image_paths)
            post_with_relations = self._post_repo.get_by_id_with_relations(
                session=session, post_id=post_id
            )
            session.flush()
        return PostResponseSchema.model_validate(obj=post_with_relations)