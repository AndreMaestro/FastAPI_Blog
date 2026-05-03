from typing import Annotated
from fastapi import Depends
from jose import jwt, JWTError

from core.exceptions.auth_exceptions import CredentialsExceptions
from core.exceptions.database_exceptions import UserNotFoundException
from infrastructure.sqlite.repositories.users import UserRepository
from resources.auth import oauth2_scheme
from infrastructure.sqlite.database import database as sqlite_database, Database
from schemas.users import UserResponseSchema
from core.config import settings

AUTH_EXCEPTION_MESSAGE = "Невозможно проверить данные авторизации"
AUTH_ALGORITHM = "HS256"
SECRET_AUTH_KEY = settings.SECRET_AUTH_KEY.get_secret_value()


class AuthService:
    @staticmethod
    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        _database: Database = sqlite_database
        _repo: UserRepository = UserRepository()

        try:
            payload = jwt.decode(
                token=token,
                key=SECRET_AUTH_KEY,
                algorithms=[AUTH_ALGORITHM],
            )
            username: str = payload.get("sub")
            if username is None:
                raise CredentialsExceptions(detail=AUTH_EXCEPTION_MESSAGE)
        except JWTError:
            raise CredentialsExceptions(detail=AUTH_EXCEPTION_MESSAGE)


        try:
            with _database.session() as session:
                user = _repo.get_by_username(session, username)
        except UserNotFoundException:
            raise CredentialsExceptions(detail=AUTH_EXCEPTION_MESSAGE)

        return UserResponseSchema.model_validate(obj=user)