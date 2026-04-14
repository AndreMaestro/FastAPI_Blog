from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from infrastructure.sqlite.repositories.base import BaseRepository, ModelType
from infrastructure.sqlite.models.locations import Location
from core.exceptions.database_exceptions import LocationNameAlreadyExistsException, LocationNotFoundException

class LocationRepository(BaseRepository[Location]):
    def __init__(self):
        super().__init__(Location, LocationNotFoundException)

    def create(self, session: Session, **data) -> Location:
        try:
            return super().create(session=session, **data)
        except IntegrityError:
            raise LocationNameAlreadyExistsException()

    def update(self, session: Session, id: int, **data) -> Location:
        try:
            obj = self.get_by_id(session, id)
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            session.flush()
            return obj
        except IntegrityError:
            raise LocationNameAlreadyExistsException()
