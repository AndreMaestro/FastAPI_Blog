from typing import List
from fastapi import APIRouter, status, Depends, Query, HTTPException

from schemas.comments import CommentResponseSchema, CommentCreateSchema, CommentUpdateSchema
from domain.comment.use_cases.get_comment_by_id import GetCommentByIdUseCase
from domain.comment.use_cases.create_comment import CreateCommentUseCase
from domain.comment.use_cases.update_comment import UpdateCommentUseCase
from domain.comment.use_cases.delete_comment import DeleteCommentUseCase
from domain.comment.use_cases.get_all_comments import GetAllCommentsUseCase
from core.exceptions.domain_exceptions import (
    CommentNotFoundByIdException, PostNotFoundByIdException, UserNotFoundByIdException
)

from api.depends import (
    get_get_comment_by_id_use_case,
    get_create_comment_use_case,
    get_update_comment_use_case,
    get_delete_comment_use_case,
    get_get_all_comments_use_case
)
from services.auth import AuthService

router = APIRouter()


@router.get('/comments', status_code=status.HTTP_200_OK, response_model=List[CommentResponseSchema])
async def get_all_comments(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    use_case: GetAllCommentsUseCase = Depends(get_get_all_comments_use_case)) -> List[CommentResponseSchema]:
    comments = await use_case.execute(limit=limit, offset=offset)
    return comments


@router.get('/comment/{comment_id}', status_code=status.HTTP_200_OK, response_model=CommentResponseSchema)
async def get_comment_by_id(
    comment_id: int,
    use_case: GetCommentByIdUseCase = Depends(get_get_comment_by_id_use_case)) -> CommentResponseSchema:
    try:
        comment = await use_case.execute(comment_id=comment_id)
    except CommentNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    return comment


@router.post('/comment', status_code=status.HTTP_201_CREATED, response_model=CommentResponseSchema)
async def create_comment(
    dto: CommentCreateSchema,
    current_user = Depends(AuthService.get_current_user),
    use_case: CreateCommentUseCase = Depends(get_create_comment_use_case)) -> CommentResponseSchema:
    dto.author_id = current_user.id
    try:
        comment = await use_case.execute(dto=dto)
    except (PostNotFoundByIdException, UserNotFoundByIdException) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=exc.get_detail()
        )
    return comment


@router.put('/comment/{comment_id}', status_code=status.HTTP_200_OK, response_model=CommentResponseSchema)
async def update_comment(
    comment_id: int,
    dto: CommentUpdateSchema,
    current_user = Depends(AuthService.get_current_user),
    get_comment_use_case: GetCommentByIdUseCase = Depends(get_get_comment_by_id_use_case),
    use_case: UpdateCommentUseCase = Depends(get_update_comment_use_case)) -> CommentResponseSchema:
    try:
        existing_comment = await get_comment_use_case.execute(comment_id=comment_id)
    except CommentNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )

    if existing_comment.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не можете обновить этот комментарий"
        )
    try:
        comment = await use_case.execute(comment_id=comment_id, dto=dto)
    except CommentNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    return comment


@router.delete('/comment/{comment_id}', status_code=status.HTTP_200_OK)
async def delete_comment(
    comment_id: int,
    current_user = Depends(AuthService.get_current_user),
    get_comment_use_case: GetCommentByIdUseCase = Depends(get_get_comment_by_id_use_case),
    use_case: DeleteCommentUseCase = Depends(get_delete_comment_use_case)) -> dict:
    try:
        existing_comment = await get_comment_use_case.execute(comment_id=comment_id)
    except CommentNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )

    if existing_comment.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не можете удалить этот комментарий"
        )

    try:
        await use_case.execute(comment_id=comment_id)
    except CommentNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    return {'message': 'Comment has been deleted'}