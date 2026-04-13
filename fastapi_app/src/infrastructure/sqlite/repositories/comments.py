from sqlalchemy.orm import Session, joinedload

from infrastructure.sqlite.repositories.base import BaseRepository
from infrastructure.sqlite.models.comments import Comment
from core.exceptions.database_exceptions import CommentNotFoundException

class CommentRepository(BaseRepository[Comment]):
    def __init__(self):
        super().__init__(Comment, CommentNotFoundException)

    def get_by_id_with_relations(
        self, session: Session, comment_id: int
    ) -> Comment | None:
        query = (
            session.query(self._model)
            .options(
                joinedload(self._model.author),
                joinedload(self._model.post),
            )
            .where(self._model.id == comment_id)
        )
        comment = query.scalar()
        if not comment:
            raise CommentNotFoundException()
        return query.scalar()