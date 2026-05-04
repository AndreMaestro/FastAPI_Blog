from infrastructure.postgres.database import database
from infrastructure.postgres.repositories.users import UserRepository
from schemas.users import UserCreateSchema, UserResponseSchema
from core.exceptions.domain_exceptions import UserIsNotUniqueByUsernameException
from core.exceptions.database_exceptions import UsernameAlreadyExistsException
from resources.auth import get_password_hash

class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, dto: UserCreateSchema) -> UserResponseSchema:
        async with self._database.session() as session:
            try:
                user = await self._repo.create(
                    session=session,
                    username = dto.username,
                    email = dto.email,
                    first_name = dto.first_name,
                    last_name = dto.last_name,
                    is_staff = dto.is_staff,
                    is_active = dto.is_active,
                    is_superuser = dto.is_superuser,
                    password = get_password_hash(dto.password)
                )
            except UsernameAlreadyExistsException:
                raise UserIsNotUniqueByUsernameException(dto.username)

            session.flush()

        return UserResponseSchema.model_validate(obj=user)