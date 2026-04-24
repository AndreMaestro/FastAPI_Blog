import logging

from core.exceptions.database_exceptions import UserNotFoundException
from core.exceptions.domain_exceptions import UserNotFoundByUsernameException, WrongPasswordException
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from resources.auth import verify_password
from schemas.users import UserResponseSchema

logger = logging.getLogger(__name__)


class AuthenticateUserUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = UserRepository()

    async def execute(self, username: str, password: str) -> UserResponseSchema:
        try:
            with self._database.session() as session:
                user = self._repo.get_by_username(session, username)
        except UserNotFoundException:
            error = UserNotFoundByUsernameException(username)
            logger.error(error.get_detail())
            raise error

        if not verify_password(plain_password=password, hashed_password=user.password):
            error = WrongPasswordException()
            logger.error(error.get_detail())
            raise error

        return UserResponseSchema.model_validate(obj=user)
