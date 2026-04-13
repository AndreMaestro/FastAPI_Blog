from mako.util import restore__ast

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import CategoryResponseSchema
from core.exceptions.domain_exceptions import CategoryNotFoundByIdException
from core.exceptions.database_exceptions import CategoryNotFoundException


class GetCategoryByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> CategoryResponseSchema:
        try:
            with self._database.session() as session:
                category = self._repo.get_by_id(session=session, id=category_id)
        except CategoryNotFoundException:
            raise CategoryNotFoundByIdException(id=category_id)

        return CategoryResponseSchema.model_validate(obj=category)