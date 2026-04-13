from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import UserSchema
from core.exceptions.database_exceptions import UserNotFoundException
from core.exceptions.domain_exceptions import UserNotFoundByUsernameException


class GetUserByUsernameUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, username: str) -> UserSchema:
        try:
            with self._database.session() as session:
                user = self._repo.get_by_username(session=session, username=username)
        except UserNotFoundException:
            raise UserNotFoundByUsernameException(username)
        return UserSchema.model_validate(obj=user)