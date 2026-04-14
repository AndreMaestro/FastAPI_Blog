from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comments import CommentRepository
from core.exceptions.domain_exceptions import CommentNotFoundByIdException
from core.exceptions.database_exceptions import CommentNotFoundException


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> bool:
        with self._database.session() as session:
            try:
                self._repo.delete(session=session, id=comment_id)
            except CommentNotFoundException:
                raise CommentNotFoundByIdException(id=comment_id)

        return True