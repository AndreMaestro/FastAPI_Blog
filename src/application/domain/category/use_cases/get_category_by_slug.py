from infrastructure.postgres.database import database
from infrastructure.postgres.repositories.categories import CategoryRepository
from schemas.categories import CategoryResponseSchema
from core.exceptions.domain_exceptions import CategoryNotFoundBySlugException
from core.exceptions.database_exceptions import CategoryNotFoundException

class GetCategoryBySlugUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, slug: str) -> CategoryResponseSchema:
        try:
            async with self._database.session() as session:
                category = await self._repo.get_by_slug(session=session, slug=slug)
        except CategoryNotFoundException:
            raise CategoryNotFoundBySlugException(slug=slug)

        return CategoryResponseSchema.model_validate(obj=category)