from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from infrastructure.sqlite.repositories.base import BaseRepository, ModelType
from infrastructure.sqlite.models.categories import Category
from core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    CategorySlugAlreadyExistsException
)

class CategoryRepository(BaseRepository[Category]):
    def __init__(self):
        super().__init__(Category, CategoryNotFoundException)

    def get_by_slug(self, session: Session, slug: str) -> Category:
        query = (
            session.query(self._model).where(self._model.slug == slug)
        )
        category = query.first()
        if category is None:
            raise CategoryNotFoundException()
        return category

    def create(self, session: Session, **data) -> Category:
        try:
            return super().create(session=session, **data)
        except IntegrityError:
            raise CategorySlugAlreadyExistsException()