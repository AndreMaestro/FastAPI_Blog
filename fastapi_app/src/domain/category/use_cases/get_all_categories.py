from typing import List

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import CategoryResponseSchema


class GetAllCategoriesUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, limit: int = 100, offset: int = 0) -> List[CategoryResponseSchema]:
        with self._database.session() as session:
            categories = self._repo.get_all(session=session, limit=limit, offset=offset)

        return [CategoryResponseSchema.model_validate(obj=cat) for cat in categories]