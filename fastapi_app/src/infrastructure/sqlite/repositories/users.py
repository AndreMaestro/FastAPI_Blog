from sqlalchemy.orm import Session
from sqlalchemy import select
from infrastructure.sqlite.repositories.base import BaseRepository
from infrastructure.sqlite.models.users import User
from core.exceptions.database_exceptions import UserNotFoundException

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User, UserNotFoundException)

    def get_by_username(self, session: Session, username: str) -> User | None:
        query = (
            select(self._model)
            .where(self._model.username == username)
        )
        user = session.scalar(query)

        if not user:
            raise UserNotFoundException

        return user