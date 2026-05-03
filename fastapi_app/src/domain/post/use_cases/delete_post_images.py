from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.images import ImageRepository
from infrastructure.sqlite.repositories.posts import PostRepository
from core.exceptions.domain_exceptions import ForbiddenException, PostNotFoundByIdException
import logging

from services.images import ImageService

logger = logging.getLogger(__name__)


class DeletePostImagesUseCase:
    def __init__(self):
        self._database = database
        self._post_repo = PostRepository()
        self._image_repo = ImageRepository()

    async def execute(self, post_id: int,
                      current_user_id: int,
                      author_id: int,
                      is_superuser: bool = False) -> None:

        if author_id != current_user_id and not is_superuser:
            error = ForbiddenException()
            logger.error("Только автор может удалять картинки")
            raise error
        with self._database.session() as session:
            post = self._post_repo.get_by_id(session=session, id=post_id)
            if not post:
                raise PostNotFoundByIdException(post_id)
            images = self._image_repo.get_images(session, "post", post_id)
            if images:
                images_paths = [img.file_path for img in images]
                self._image_repo.delete_images(session, "post", post_id)
                await ImageService.delete_images(images_paths)