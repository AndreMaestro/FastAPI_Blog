from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.postgres.repositories.base import BaseRepository, ModelType
from infrastructure.postgres.models.locations import Location
from core.exceptions.database_exceptions import LocationNameAlreadyExistsException, LocationNotFoundException

class LocationRepository(BaseRepository[Location]):
    def __init__(self):
        super().__init__(Location, LocationNotFoundException)

    async def create(self, session: AsyncSession, **data) -> Location:
        try:
            return await super().create(session=session, **data)
        except IntegrityError:
            raise LocationNameAlreadyExistsException()

    async def update(self, session: AsyncSession, id: int, **data) -> Location:
        try:
            obj = await self.get_by_id(session, id)
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            await session.flush()
            return obj
        except IntegrityError:
            raise LocationNameAlreadyExistsException()
