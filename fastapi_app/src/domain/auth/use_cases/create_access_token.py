from datetime import timedelta, datetime, timezone
from jose import jwt
from services.auth import SECRET_AUTH_KEY, AUTH_ALGORITHM

class CreateAccessTokenUseCase:
    def __init__(self, token_expire_minutes: int = 5) -> None:
        self._ACCESS_TOKEN_EXPIRE_MINUTES = token_expire_minutes

    async def execute(
            self,
            username: str,
            expires_delta: timedelta | None = None
    ) -> str:
        to_encode = {"sub": username}
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=self._ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            claims=to_encode,
            key=SECRET_AUTH_KEY,
            algorithm=AUTH_ALGORITHM,
        )

        return encoded_jwt
