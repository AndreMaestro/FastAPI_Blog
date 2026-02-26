from http.client import responses, HTTPResponse

from fastapi import APIRouter, status, HTTPException
from fastapi.openapi.utils import status_code_ranges

from ..schemas.posts import PostCreateSchema, PostUpdateSchema, PostResponseSchema


router = APIRouter()


DataBase = []

@router.get("/get/{post_id}")
def get_post(post_id: int):
    if post_id < len(DataBase):
        return DataBase[post_id]
    else:
        raise HTTPException(
            detail="Публикация не найдена",
            status_code = status.HTTP_404_NOT_FOUND,
        )


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=PostResponseSchema,
)


def create_post(post: PostCreateSchema):
    response ={
        "title": post.title,
        "text": post.text,
        "author": post.author,
        "pub_date": post.pub_date,
        "location": post.location,
        "category": post.category,
        "is_published": post.is_published,
        "created_at": post.created_at,
        "id": len(DataBase),
    }
    DataBase.append(response)
    return PostResponseSchema.model_validate(obj=response)


@router.put(
    "/update/{post_id}",
    status_code=status.HTTP_200_OK,
    response_model=PostUpdateSchema,
)


def update_post(post_id: int, post: PostUpdateSchema):
    if post_id > len(DataBase):
        raise HTTPException(
            detail='Публикация не найдена',
            status_code=status.HTTP_404_NOT_FOUND,
        )

    response = DataBase[post_id]
    response['title'] = post.title
    response['text'] = post.text
    response['location'] = post.location
    response['category'] = post.category
    response['is_published'] = post.is_published

    return PostUpdateSchema.model_validate(obj=response)


@router.delete(
    "/delete/{post_id}",
    status_code=status.HTTP_200_OK,
)


def delete_post(post_id: int):
    if post_id > len(DataBase):
        raise HTTPException(
            detail='Публикация не найдена',
            status_code=status.HTTP_404_NOT_FOUND,
        )
    DataBase.pop(post_id)
    return{'message': 'Публикация удалена'}
