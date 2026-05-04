from typing import List

from infrastructure.postgres.database import database
from infrastructure.postgres.repositories.locations import LocationRepository
from schemas.locations import LocationResponseSchema


class GetAllLocationsUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, limit: int = 100, offset: int = 0) -> List[LocationResponseSchema]:
        async with self._database.session() as session:
            locations = await self._repo.get_all(session=session, limit=limit, offset=offset)

        return [LocationResponseSchema.model_validate(obj=loc) for loc in locations]