from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import LocationResponseSchema, LocationCreateUpdateSchema
from core.exceptions.domain_exceptions import (
    LocationNameIsNotUniqueException,
    LocationNotFoundByIdException,
)
from core.exceptions.database_exceptions import (
    LocationNameAlreadyExistsException,
    LocationNotFoundException,
)


class UpdateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int, dto: LocationCreateUpdateSchema) -> LocationResponseSchema:
        with self._database.session() as session:
            try:
                location = self._repo.update(
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