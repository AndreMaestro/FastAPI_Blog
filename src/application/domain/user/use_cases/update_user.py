from infrastructure.postgres.database import database
from infrastructure.postgres.repositories.users import UserRepository
from schemas.users import UserCreateSchema, UserResponseSchema
from core.exceptions.domain_exceptions import UserNotFoundByIdException, UserIsNotUniqueByUsernameException, \
    ForbiddenException
from core.exceptions.database_exceptions import UsernameAlreadyExistsException, UserNotFoundException
import logging

logger = logging.getLogger(__name__)


class UpdateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int, dto: UserCreateSchema, current_user_id: int) -> UserResponseSchema:
        if user_id != current_user_id:
            error = ForbiddenException()
            logger.error("Пользователь может редактировать только свой профиль")
            raise error
        async with self._database.session as session:
            try:
                await self._repo.get_by_id(session, user_id)
            except UserNotFoundException:
                raise UserNotFoundByIdException(user_id)

            try:
                user = await self._repo.update(
                    session=session,
                    id = user_id,
                    username = dto.username,
                    email = dto.email,
                    first_name = dto.first_name,
                    last_name = dto.last_name,
                    is_staff = dto.is_staff,
                    is_active = dto.is_active,
                    is_superuser = dto.is_superuser,
                    password = dto.password
                )
            except UsernameAlreadyExistsException:
                raise UserIsNotUniqueByUsernameException(dto.username)

            session.flush()

        return UserResponseSchema.model_validate(obj=user)