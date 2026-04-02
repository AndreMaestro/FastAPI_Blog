from sqlalchemy.orm import Session

from infrastructure.sqlite.repositories.base import BaseRepository
from infrastructure.sqlite.models.users import User


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_username(self, session: Session, username: str) -> User | None:
        return (
            session.query(self._model)
            .where(self._model.username == username)
            .scalar()
        )