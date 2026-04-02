from sqlalchemy.orm import Session

from infrastructure.sqlite.repositories.base import BaseRepository
from infrastructure.sqlite.models.categories import Category


class CategoryRepository(BaseRepository[Category]):
    def __init__(self):
        super().__init__(Category)

    def get_by_slug(self, session: Session, slug: str) -> Category | None:
        return (
            session.query(self._model).where(self._model.slug == slug).scalar()
        )