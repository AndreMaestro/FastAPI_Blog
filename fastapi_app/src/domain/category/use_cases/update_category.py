from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import CategoryResponseSchema, CategoryUpdateSchema
from core.exceptions.domain_exceptions import CategoryNotFoundByIdException
from core.exceptions.database_exceptions import CategoryNotFoundException


class UpdateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int, dto: CategoryUpdateSchema) -> CategoryResponseSchema:
        with self._database.session() as session:
            try:
                category = self._repo.update(
                    session=session,
                    id=category_id,
                    title=dto.title,
                    description=dto.description,
                    is_published=dto.is_published,
                )
            except CategoryNotFoundException:
                raise CategoryNotFoundByIdException(id=category_id)

        return CategoryResponseSchema.model_validate(obj=category)