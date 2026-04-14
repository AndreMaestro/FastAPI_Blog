from datetime import datetime

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comments import CommentRepository
from infrastructure.sqlite.repositories.posts import PostRepository
from infrastructure.sqlite.repositories.users import UserRepository
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
        with self._database.session() as session:
            try:
                post = self._post_repo.get_by_id(session, dto.post_id)
            except PostNotFoundException:
                raise PostNotFoundByIdException(dto.post_id)

            try:
                user = self._user_repo.get_by_id(session, dto.author_id)
            except UserNotFoundException:
                raise UserNotFoundByIdException(id=dto.author_id)

            comment = self._repo.create(
                session=session,
                text=dto.text,
                author_id=dto.author_id,
                post_id=dto.post_id,
                created_at=datetime.now(),
            )
            session.flush()
            comment_with_relations = self._repo.get_by_id_with_relations(
                session=session, comment_id=comment.id
            )

        return CommentResponseSchema.model_validate(obj=comment_with_relations)