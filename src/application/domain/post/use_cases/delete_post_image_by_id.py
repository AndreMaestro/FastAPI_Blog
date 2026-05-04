import logging

from infrastructure.postgres.database import database
from infrastructure.postgres.repositories.posts import PostRepository
from infrastructure.postgres.repositories.images import ImageRepository
from services.images import ImageService
from core.exceptions.domain_exceptions import ForbiddenException, PostNotFoundByIdException
from core.exceptions.database_exceptions import ImageNotFoundException

logger = logging.getLogger(__name__)


class DeletePostImageByIdUseCase:
    def __init__(self):
        self._database = database
        self._post_repo = PostRepository()
        self._image_repo = ImageRepository()

    async def execute(
            self,
            post_id: int,
            image_id: int,
            current_user_id: int,
            author_id: int,
            is_superuser: bool = False
    ) -> None:
        if author_id != current_user_id and not is_superuser:
            error = ForbiddenException()
            logger.error("Только автор может удалять картинки")
            raise error

        async with self._database.session() as session:
            post = await self._post_repo.get_by_id(session, post_id)
            if not post:
                raise PostNotFoundByIdException(post_id)

            image = await self._image_repo.get_by_id(session, image_id)
            if not image or image.object_id != post_id or image.content_type != "post":
                raise ImageNotFoundException(image_id)

            await ImageService.delete_image(image.file_path)

            session.delete(image)
            session.flush()