from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from core.exceptions.domain_exceptions import UserNotFoundByIdException, ForbiddenException
from core.exceptions.database_exceptions import UserNotFoundException
import logging

logger = logging.getLogger(__name__)


class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int, current_user_id: int, is_superuser: bool = False) -> bool:
        if user_id != current_user_id and not is_superuser:
            error = ForbiddenException()
            logger.error("Только пользователь (или администратор) может удалять свой профиль")
            raise error
        try:
            with self._database.session() as session:
                self._repo.delete(session=session, id=user_id)
        except UserNotFoundException:
            raise UserNotFoundByIdException(id=user_id)

        return True