from datetime import datetime

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import CategoryResponseSchema, CategoryCreateSchema


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, dto: CategoryCreateSchema) -> CategoryResponseSchema:
        with self._database.session() as session:
            category = self._repo.create(
                session=session,
                title=dto.title,
                description=dto.description,
                slug=dto.slug,
                is_published=dto.is_published,
                created_at=datetime.now(),
            )
            session.flush()

        return CategoryResponseSchema.model_validate(obj=category)