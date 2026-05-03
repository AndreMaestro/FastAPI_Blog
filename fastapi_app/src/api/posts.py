from typing import List, Annotated
from fastapi import APIRouter, status, Depends, Query, HTTPException, UploadFile, File

from domain.post.use_cases.add_post_images import AddPostImagesUseCase
from domain.post.use_cases.delete_post_images import DeletePostImagesUseCase
from domain.post.use_cases.delete_post_image_by_id import DeletePostImageByIdUseCase
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
    UserNotFoundByIdException, ForbiddenException
)

from api.depends import (
    get_get_post_by_id_use_case,
    get_create_post_use_case,
    get_update_post_use_case,
    get_delete_post_use_case,
    get_get_all_posts_use_case,
    get_add_post_images_use_case,
    get_delete_post_images_use_case,
    get_delete_post_image_by_id_use_case
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
        current_user=Depends(AuthService.get_current_user),
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
        current_user=Depends(AuthService.get_current_user),
        get_post_use_case: GetPostByIdUseCase = Depends(get_get_post_by_id_use_case),
        use_case: UpdatePostUseCase = Depends(get_update_post_use_case)) -> PostResponseSchema:
    try:
        existing_post = await get_post_use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail()
        )
    try:
        post = await use_case.execute(post_id=post_id,
                                      dto=dto,
                                      author_id=existing_post.author.id,
                                      current_user_id=current_user.id
                                      )
    except ForbiddenException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=exc.get_detail()
        )
    except (CategoryNotFoundByIdException, LocationNotFoundByIdException) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=exc.get_detail()
        )
    return post


@router.delete('/post/{post_id}', status_code=status.HTTP_200_OK)
async def delete_post(
        post_id: int,
        current_user=Depends(AuthService.get_current_user),
        get_post_use_case: GetPostByIdUseCase = Depends(get_get_post_by_id_use_case),
        use_case: DeletePostUseCase = Depends(get_delete_post_use_case)) -> dict:
    try:
        existing_post = await get_post_use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )

    await use_case.execute(post_id=post_id,
                           author_id=existing_post.author.id,
                           current_user_id=current_user.id,
                           is_superuser=current_user.is_superuser)
    return {'message': 'Post has been deleted'}


@router.post('/post/{post_id}/images', status_code=status.HTTP_200_OK, response_model=PostResponseSchema)
async def upload_post_images(
    post_id: int,
    # не работает List[UploadFile]
    images: UploadFile = File(...),
    current_user=Depends(AuthService.get_current_user),
    get_post_use_case: GetPostByIdUseCase = Depends(get_get_post_by_id_use_case),
    use_case: AddPostImagesUseCase = Depends(get_add_post_images_use_case)
) -> PostResponseSchema:
    try:
        existing_post = await get_post_use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )

    try:
        list_images = []
        list_images.append(images)
        updated_post = await use_case.execute(
            post_id=post_id,
            images=list_images,
            current_user_id=current_user.id,
            author_id=existing_post.author.id
        )
    except ForbiddenException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=exc.get_detail()
        )

    return updated_post


@router.delete('/post/{post_id}/images', status_code=status.HTTP_200_OK)
async def delete_post_images(
        post_id: int,
        current_user=Depends(AuthService.get_current_user),
        get_post_use_case: GetPostByIdUseCase = Depends(get_get_post_by_id_use_case),
        use_case: DeletePostImagesUseCase = Depends(get_delete_post_images_use_case)
) -> dict:
    try:
        existing_post = await get_post_use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )

    await use_case.execute(
        post_id=post_id,
        current_user_id=current_user.id,
        author_id=existing_post.author.id,
        is_superuser=current_user.is_superuser
    )

    return {"message": f"All images for post {post_id} have been deleted"}


@router.delete('/post/{post_id}/images/{image_id}', status_code=status.HTTP_200_OK)
async def delete_post_image_by_id(
        post_id: int,
        image_id: int,
        current_user=Depends(AuthService.get_current_user),
        get_post_use_case: GetPostByIdUseCase = Depends(get_get_post_by_id_use_case),
        use_case: DeletePostImageByIdUseCase = Depends(get_delete_post_image_by_id_use_case)
) -> dict:
    try:
        existing_post = await get_post_use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )

    await use_case.execute(
        post_id=post_id,
        image_id=image_id,
        current_user_id=current_user.id,
        author_id=existing_post.author.id,
        is_superuser=current_user.is_superuser
    )

    return {"message": f"Image {image_id} for post {post_id} has been deleted"}