from infrastructure.postgres.database import database
from infrastructure.postgres.repositories.categories import CategoryRepository
from schemas.categories import CategoryResponseSchema, CategoryUpdateSchema
from core.exceptions.domain_exceptions import CategoryNotFoundByIdException, ForbiddenException
from core.exceptions.database_exceptions import CategoryNotFoundException
import logging

logger = logging.getLogger(__name__)


class UpdateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int, dto: CategoryUpdateSchema, is_superuser: bool = False) -> CategoryResponseSchema:
        if not is_superuser:
            error = ForbiddenException()
            logger.error("Только администратор может обновлять категории")
            raise error
        async with self._database.session() as session:
            try:
                category = await self._repo.update(
                    session=session,
                    id=category_id,
                    title=dto.title,
                    description=dto.description,
                    is_published=dto.is_published,
                )
            except CategoryNotFoundException:
                raise CategoryNotFoundByIdException(id=category_id)

        return CategoryResponseSchema.model_validate(obj=category)