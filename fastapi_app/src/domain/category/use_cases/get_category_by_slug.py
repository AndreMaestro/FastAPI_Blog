from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import CategoryResponseSchema
from core.exceptions.domain_exceptions import CategoryNotFoundBySlugException
from core.exceptions.database_exceptions import CategoryNotFoundException

class GetCategoryBySlugUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, slug: str) -> CategoryResponseSchema:
        try:
            with self._database.session() as session:
                category = self._repo.get_by_slug(session=session, slug=slug)
        except CategoryNotFoundException:
            raise CategoryNotFoundBySlugException(slug=slug)

        return CategoryResponseSchema.model_validate(obj=category)