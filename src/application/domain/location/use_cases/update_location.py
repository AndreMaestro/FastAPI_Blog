from infrastructure.postgres.database import database
from infrastructure.postgres.repositories.locations import LocationRepository
from schemas.locations import LocationResponseSchema, LocationCreateUpdateSchema
from core.exceptions.domain_exceptions import (
    LocationNameIsNotUniqueException,
    LocationNotFoundByIdException, ForbiddenException,
)
from core.exceptions.database_exceptions import (
    LocationNameAlreadyExistsException,
    LocationNotFoundException,
)
import logging

logger = logging.getLogger(__name__)


class UpdateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int, dto: LocationCreateUpdateSchema, is_superuser: bool = False) -> LocationResponseSchema:
        if not is_superuser:
            error = ForbiddenException()
            logger.error("Только администратор может обновлять локации")
            raise error
        async with self._database.session() as session:
            try:
                location = await self._repo.update(
                    session=session,
                    id=location_id,
                    name=dto.name,
                    is_published=dto.is_published,
                )
            except LocationNotFoundException:
                raise LocationNotFoundByIdException(location_id)
            except LocationNameAlreadyExistsException:
                raise LocationNameIsNotUniqueException(dto.name)

        return LocationResponseSchema.model_validate(obj=location)