from datetime import datetime

from infrastructure.postgres.database import database
from infrastructure.postgres.repositories.comments import CommentRepository
from infrastructure.postgres.repositories.posts import PostRepository
from infrastructure.postgres.repositories.users import UserRepository
from schemas.comments import CommentResponseSchema, CommentCreateSchema
from core.exceptions.domain_exceptions import PostNotFoundByIdException, UserNotFoundByIdException
from core.exceptions.database_exceptions import PostNotFoundException, UserNotFoundException


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._post_repo = PostRepository()
        self._user_repo = UserRepository()

    async def execute(self, dto: CommentCreateSchema) -> CommentResponseSchema:
        async with self._database.session() as session:
            try:
                post = await self._post_repo.get_by_id(session, dto.post_id)
            except PostNotFoundException:
                raise PostNotFoundByIdException(dto.post_id)

            try:
                user = await self._user_repo.get_by_id(session, dto.author_id)
            except UserNotFoundException:
                raise UserNotFoundByIdException(id=dto.author_id)

            comment = await self._repo.create(
                session=session,
                text=dto.text,
                author_id=dto.author_id,
                post_id=dto.post_id,
                created_at=datetime.now(),
            )
            session.flush()
            comment_with_relations = await self._repo.get_by_id_with_relations(
                session=session, comment_id=comment.id
            )

        return CommentResponseSchema.model_validate(obj=comment_with_relations)