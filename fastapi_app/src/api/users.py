from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from schemas.users import *

from domain.user.use_cases.get_user_by_username import GetUserByUsernameUseCase
from domain.user.use_cases.create_user import CreateUserUseCase
from domain.user.use_cases.update_user import UpdateUserUseCase
from domain.user.use_cases.delete_user import DeleteUserUseCase
from domain.user.use_cases.get_all_users import GetAllUsersUseCase
from core.exceptions.domain_exceptions import (
    UserNotFoundByUsernameException,
    UserIsNotUniqueByUsernameException,
    UserNotFoundByIdException
)
from api.depends import (
    get_get_user_by_username_use_case,
    get_create_user_use_case,
    get_update_user_use_case,
    get_delete_user_use_case,
    get_get_all_users_use_case
)
from services.auth import AuthService

router = APIRouter()


@router.get('/user/{username}', status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
async def get_user_by_username(
    username: str,
    use_case: GetUserByUsernameUseCase = Depends(get_get_user_by_username_use_case),
) -> UserResponseSchema:
    try:
        user = await use_case.execute(username=username)
    except UserNotFoundByUsernameException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    return user


@router.get("/users/", status_code=status.HTTP_200_OK, response_model=List[UserResponseSchema])
async def get_all_users(
    offset: int = 0,
    limit: int = 100,
    use_case: GetAllUsersUseCase = Depends(get_get_all_users_use_case),
) -> List[UserResponseSchema]:
    users = await use_case.execute(offset=offset, limit=limit)
    return users


@router.post('/user/', status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
async def create_user(
    dto: UserCreateSchema,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
) -> UserResponseSchema:
    try:
        user = await use_case.execute(dto=dto)
    except UserIsNotUniqueByUsernameException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail()
        )
    return user


@router.put('/user/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
async def update_user(
        user_id: int,
        dto: UserUpdateSchema,
        current_user=Depends(AuthService.get_current_user),
        use_case: UpdateUserUseCase = Depends(get_update_user_use_case),
) -> UserResponseSchema:
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не можете редактировать другого пользователя"
        )

    try:
        user = await use_case.execute(user_id=user_id, dto=dto)
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    except UserIsNotUniqueByUsernameException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail()
        )
    return user


@router.delete('/user/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
async def delete_user(
        user_id: int,
        current_user = Depends(AuthService.get_current_user),
        use_case: DeleteUserUseCase = Depends(get_delete_user_use_case)
) -> None:
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= "Вы не можете удалять чужого пользователя"
        )

    try:
        await use_case.execute(user_id)
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    return None