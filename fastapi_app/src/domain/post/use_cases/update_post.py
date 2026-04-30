from sqlalchemy.exc import IntegrityError

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.posts import PostRepository
from infrastructure.sqlite.repositories.locations import LocationRepository
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.posts import PostResponseSchema, PostUpdateSchema
from core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    LocationNotFoundByIdException,
    CategoryNotFoundByIdException, ForbiddenException
)
from core.exceptions.database_exceptions import(
    CategoryNotFoundException,
    LocationNotFoundException
)
import logging

logger = logging.getLogger(__name__)


class UpdatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._location_repo = LocationRepository()
        self._category_repo = CategoryRepository()

    async def execute(self,
                      post_id: int,
                      dto: PostUpdateSchema,
                      author_id: int,
                      current_user_id: int) -> PostResponseSchema:
        if author_id != current_user_id:
            error = ForbiddenException()
            logger.error("Только автор поста может обновлять его")
            raise error

        with self._database.session() as session:
            try:
                self._category_repo.get_by_id(session, dto.category_id)
            except CategoryNotFoundException:
                raise CategoryNotFoundByIdException(dto.category_id)
            
            try:
                self._location_repo.get_by_id(session, dto.location_id)
            except LocationNotFoundException:
                raise LocationNotFoundByIdException(dto.location_id)

            try:
                post = self._repo.update(
                    session=session,
                    id=post_id,
                    title=dto.title,
                    text=dto.text,
                    is_published=dto.is_published,
                    category_id=dto.category_id,
                    location_id=dto.location_id,
                )
            except IntegrityError:
                raise PostNotFoundByIdException(post_id)

            post_with_relations = self._repo.get_by_id_with_relations(
                session=session, post_id=post_id
            )

        return PostResponseSchema.model_validate(obj=post_with_relations)