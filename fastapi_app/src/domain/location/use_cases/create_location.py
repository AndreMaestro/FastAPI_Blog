from datetime import datetime

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import LocationResponseSchema, LocationCreateUpdateSchema
from core.exceptions.domain_exceptions import LocationNameIsNotUniqueException
from core.exceptions.database_exceptions import LocationNameAlreadyExistsException


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, dto: LocationCreateUpdateSchema) -> LocationResponseSchema:
        with self._database.session() as session:
            try:
                location = self._repo.create(
                    session=session,
                    name=dto.name,
                    is_published=dto.is_published,
                    created_at=datetime.now(),
                )
            except LocationNameAlreadyExistsException:
                raise LocationNameIsNotUniqueException(dto.name)

        return LocationResponseSchema.model_validate(obj=location)