from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import CategoryResponseSchema, CategoryUpdateSchema


class UpdateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int, dto: CategoryUpdateSchema) -> CategoryResponseSchema:
        with self._database.session() as session:
            category = self._repo.update(
                session=session,
                id=category_id,
                title=dto.title,
                description=dto.description,
                is_published=dto.is_published,
            )

            if category is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Category with id {category_id} not found',
                )

        return CategoryResponseSchema.model_validate(obj=category)