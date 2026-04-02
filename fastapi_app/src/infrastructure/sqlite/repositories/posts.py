from sqlalchemy.orm import Session, joinedload

from infrastructure.sqlite.repositories.base import BaseRepository
from infrastructure.sqlite.models.posts import Post


class PostRepository(BaseRepository[Post]):
    def __init__(self):
        super().__init__(Post)

    def get_all(
        self, session: Session, limit: int = 100, offset: int = 0
    ) -> list[Post]:
        query = (
            session.query(self._model)
            .options(
                joinedload(self._model.author),
                joinedload(self._model.category),
                joinedload(self._model.location),
            )
            .limit(limit)
            .offset(offset)
            .all()
        )
        return query

    def get_by_id_with_relations(
        self, session: Session, post_id: int
    ) -> Post | None:
        query = (
            session.query(self._model)
            .options(
                joinedload(self._model.author),
                joinedload(self._model.category),
                joinedload(self._model.location),
            )
            .where(self._model.id == post_id)
        )
        return query.scalar()