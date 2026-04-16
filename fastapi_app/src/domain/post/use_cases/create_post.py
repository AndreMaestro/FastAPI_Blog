from datetime import datetime
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.posts import PostRepository
from infrastructure.sqlite.repositories.locations import LocationRepository
from infrastructure.sqlite.repositories.categories import CategoryRepository
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.posts import PostResponseSchema, PostCreateSchema
from core.exceptions.domain_exceptions import (
    LocationNotFoundByIdException,
    CategoryNotFoundByIdException,
    UserNotFoundByIdException
)
from core.exceptions.database_exceptions import(
    CategoryNotFoundException,
    LocationNotFoundException,
    UserNotFoundException
)

class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._location_repo = LocationRepository()
        self._category_repo = CategoryRepository()
        self._user_repo = UserRepository()

    async def execute(self, dto: PostCreateSchema) -> PostResponseSchema:
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
                self._user_repo.get_by_id(session, dto.author_id)
            except UserNotFoundException:
                raise UserNotFoundByIdException(dto.author_id)

            post = self._repo.create(
                session=session,
                title=dto.title,
                text=dto.text,
                is_published=dto.is_published,
                created_at=datetime.now(),
                pub_date=dto.pub_date,
                author_id=dto.author_id,
                category_id=dto.category_id,
                location_id=dto.location_id,
                image=dto.image or '',
            )
            session.flush()
            post_with_relations = self._repo.get_by_id_with_relations(
                session=session, post_id=post.id
            )
        return PostResponseSchema.model_validate(obj=post_with_relations)