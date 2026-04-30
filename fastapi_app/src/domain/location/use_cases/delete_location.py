from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from core.exceptions.domain_exceptions import LocationNotFoundByIdException, ForbiddenException
from core.exceptions.database_exceptions import LocationNotFoundException
import logging

logger = logging.getLogger(__name__)


class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int, is_superuser: bool = False) -> bool:
        if not is_superuser:
            error = ForbiddenException()
            logger.error("Только администратор может удалять локации")
            raise error
        with self._database.session() as session:
            try:
                self._repo.delete(session=session, id=location_id)
            except LocationNotFoundException:
                raise LocationNotFoundByIdException(id=location_id)

        return True