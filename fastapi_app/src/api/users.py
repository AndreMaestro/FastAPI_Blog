from fastapi import APIRouter, status, Depends, HTTPException

from schemas.users import UserSchema
from domain.user.use_cases.get_user_by_username import GetUserByUsernameUseCase
from core.exceptions.domain_exceptions import UserNotFoundByUsernameException
from api.depends import get_get_user_by_username_use_case

router = APIRouter()


@router.get('/user/{username}', status_code=status.HTTP_200_OK, response_model=UserSchema)
async def get_user_by_username(
    username: str,
    use_case: GetUserByUsernameUseCase = Depends(get_get_user_by_username_use_case),
) -> UserSchema:
    try:
        user = await use_case.execute(username=username)
    except UserNotFoundByUsernameException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    return user