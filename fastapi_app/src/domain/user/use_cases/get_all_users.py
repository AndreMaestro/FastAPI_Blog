from typing import List

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import UserResponseSchema


class GetAllUsersUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, limit: int = 100, offset: int = 0) -> List[UserResponseSchema]:
        with self._database.session() as session:
            posts = self._repo.get_all(session=session, limit=limit, offset=offset)
        return [UserResponseSchema.model_validate(obj=post) for post in posts]