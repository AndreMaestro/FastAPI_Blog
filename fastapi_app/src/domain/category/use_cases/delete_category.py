from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from core.exceptions.domain_exceptions import CategoryNotFoundByIdException,ForbiddenException
from core.exceptions.database_exceptions import CategoryNotFoundException
import logging

logger = logging.getLogger(__name__)


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int, is_superuser: bool =False) -> bool:
        if not is_superuser:
            error = ForbiddenException()
            logger.error("Только администратор может удалять категории")
            raise error

        with self._database.session() as session:
            try:
                self._repo.delete(session=session, id=category_id)
            except CategoryNotFoundException:
                raise CategoryNotFoundByIdException(id=category_id)

        return True