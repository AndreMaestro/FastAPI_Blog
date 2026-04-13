from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository


class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> bool:
        with self._database.session() as session:
            self._repo.delete(session=session, id=location_id)

        return True