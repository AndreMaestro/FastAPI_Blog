from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from core.exceptions.domain_exceptions import CategoryNotFoundByIdException
from core.exceptions.database_exceptions import CategoryNotFoundException


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> bool:
        with self._database.session() as session:
            try:
                self._repo.delete(session=session, id=category_id)
            except CategoryNotFoundException:
                raise CategoryNotFoundByIdException(id=category_id)

        return True