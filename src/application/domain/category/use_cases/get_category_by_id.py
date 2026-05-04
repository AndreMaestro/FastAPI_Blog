from infrastructure.postgres.database import database
from infrastructure.postgres.repositories.categories import CategoryRepository
from schemas.categories import CategoryResponseSchema
from core.exceptions.domain_exceptions import CategoryNotFoundByIdException
from core.exceptions.database_exceptions import CategoryNotFoundException


class GetCategoryByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> CategoryResponseSchema:
        try:
            async with self._database.session() as session:
                category = await self._repo.get_by_id(session=session, id=category_id)
        except CategoryNotFoundException:
            raise CategoryNotFoundByIdException(id=category_id)

        return CategoryResponseSchema.model_validate(obj=category)