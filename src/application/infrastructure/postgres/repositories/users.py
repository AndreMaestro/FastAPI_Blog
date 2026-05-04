from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from infrastructure.postgres.repositories.base import BaseRepository
from infrastructure.postgres.models.users import User
from core.exceptions.database_exceptions import UserNotFoundException

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User, UserNotFoundException)

    async def get_by_username(self, session: AsyncSession, username: str) -> User | None:
        query = (
            select(self._model)
            .where(self._model.username == username)
        )
        user = await session.scalar(query)

        if not user:
            raise UserNotFoundException

        return user