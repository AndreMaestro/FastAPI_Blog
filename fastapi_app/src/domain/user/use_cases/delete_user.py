from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from core.exceptions.domain_exceptions import UserNotFoundByIdException
from core.exceptions.database_exceptions import UserNotFoundException


class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> bool:
        try:
            with self._database.session() as session:
                self._repo.delete(session=session, id=user_id)
        except UserNotFoundException:
            raise UserNotFoundByIdException(id=user_id)

        return True