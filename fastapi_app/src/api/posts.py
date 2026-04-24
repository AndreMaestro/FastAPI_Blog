from typing import List
from fastapi import APIRouter, status, Depends, Query, HTTPException

from schemas.posts import PostResponseSchema, PostCreateSchema, PostUpdateSchema
from domain.post.use_cases.get_post_by_id import GetPostByIdUseCase
from domain.post.use_cases.create_post import CreatePostUseCase
from domain.post.use_cases.update_post import UpdatePostUseCase
from domain.post.use_cases.delete_post import DeletePostUseCase
from domain.post.use_cases.get_all_posts import GetAllPostsUseCase
from services.auth import AuthService
from core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    CategoryNotFoundByIdException,
    LocationNotFoundByIdException,
    UserNotFoundByIdException
)

from api.depends import (
    get_get_post_by_id_use_case,
    get_create_post_use_case,
    get_update_post_use_case,
    get_delete_post_use_case,
    get_get_all_posts_use_case
)

router = APIRouter()


@router.get('/posts', status_code=status.HTTP_200_OK, response_model=List[PostResponseSchema])
async def get_all_posts(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    use_case: GetAllPostsUseCase = Depends(get_get_all_posts_use_case)) -> List[PostResponseSchema]:
    posts = await use_case.execute(limit=limit, offset=offset)
    return posts


@router.get('/post/{post_id}', status_code=status.HTTP_200_OK, response_model=PostResponseSchema)
async def get_post_by_id(
    post_id: int,
    use_case: GetPostByIdUseCase = Depends(get_get_post_by_id_use_case)) -> PostResponseSchema:
    try:
        post = await use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    return post


@router.post('/post', status_code=status.HTTP_201_CREATED, response_model=PostResponseSchema)
async def create_post(
    dto: PostCreateSchema,
    current_user = Depends(AuthService.get_current_user),
    use_case: CreatePostUseCase = Depends(get_create_post_use_case)) -> PostResponseSchema:
    dto.author_id = current_user.id
    try:
        post = await use_case.execute(dto=dto)
    except(CategoryNotFoundByIdException, LocationNotFoundByIdException, UserNotFoundByIdException) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=exc.get_detail()
        )
    return post


@router.put('/post/{post_id}', status_code=status.HTTP_200_OK, response_model=PostResponseSchema)
async def update_post(
    post_id: int,
    dto: PostUpdateSchema,
    current_user = Depends(AuthService.get_current_user),
    get_post_use_case: GetPostByIdUseCase = Depends(get_get_post_by_id_use_case),
    use_case: UpdatePostUseCase = Depends(get_update_post_use_case)) -> PostResponseSchema:
    try:
        existing_post = await get_post_use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail()
        )
    if existing_post.author.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Вы не можете обновить этот пост'
        )
    try:
        post = await use_case.execute(post_id=post_id, dto=dto)
    except (CategoryNotFoundByIdException, LocationNotFoundByIdException) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=exc.get_detail()
        )
    return post


@router.delete('/post/{post_id}', status_code=status.HTTP_200_OK)
async def delete_post(
    post_id: int,
    current_user = Depends(AuthService.get_current_user),
    get_post_use_case: GetPostByIdUseCase = Depends(get_get_post_by_id_use_case),
    use_case: DeletePostUseCase = Depends(get_delete_post_use_case)) -> dict:
    try:
        existing_post = await get_post_use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    if existing_post.author.id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Вы не можете удалить этот пост'
        )
    await use_case.execute(post_id=post_id)
    return {'message': 'Post has been deleted'}