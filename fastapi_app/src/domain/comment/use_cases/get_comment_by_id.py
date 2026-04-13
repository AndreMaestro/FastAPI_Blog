from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comments import CommentRepository
from schemas.comments import CommentResponseSchema
from core.exceptions.domain_exceptions import CommentNotFoundByIdException
from core.exceptions.database_exceptions import CommentNotFoundException


class GetCommentByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> CommentResponseSchema:
        try:
            with self._database.session() as session:
                comment = self._repo.get_by_id_with_relations(session=session, comment_id=comment_id)
        except CommentNotFoundException:
            raise CommentNotFoundByIdException(id=comment_id)

        return CommentResponseSchema.model_validate(obj=comment)