from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> bool:
        with self._database.session() as session:
            self._repo.delete(session=session, id=category_id)

        return True