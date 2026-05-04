from infrastructure.postgres.database import database
from infrastructure.postgres.repositories.users import UserRepository
from schemas.users import UserResponseSchema
from core.exceptions.database_exceptions import UserNotFoundException
from core.exceptions.domain_exceptions import UserNotFoundByUsernameException


class GetUserByUsernameUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, username: str) -> UserResponseSchema:
        try:
            async with self._database.session() as session:
                user = await self._repo.get_by_username(session=session, username=username)
        except UserNotFoundException:
            raise UserNotFoundByUsernameException(username)
        return UserResponseSchema.model_validate(obj=user)