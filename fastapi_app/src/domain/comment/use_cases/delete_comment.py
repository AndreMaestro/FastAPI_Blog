from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comments import CommentRepository


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> bool:
        with self._database.session() as session:
            self._repo.delete(session=session, id=comment_id)

        return True