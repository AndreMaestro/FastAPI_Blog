from sqlalchemy.orm import Session, joinedload

from infrastructure.sqlite.repositories.base import BaseRepository
from infrastructure.sqlite.models.comments import Comment


class CommentRepository(BaseRepository[Comment]):
    def __init__(self):
        super().__init__(Comment)

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
        return query.scalar()