from fastapi import HTTPException, status
from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from .users import UserResponseSchema
from typing import List


class ImageSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    file_path: str
    order: int


class PostBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str = Field(min_length=1, max_length=256, description='Заголовок')
    text: str = Field(min_length=1, description='Текст')
    location_id: int | None = Field(None, description='Местоположение')
    category_id: int | None = Field(None, description='Категория')

    @field_validator("title", mode='after')
    @staticmethod
    def validate_title(title: str) -> str:
        if not title.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Заголовок поста не должен состоять только из пробелов"
            )
        return title


class PostCreateSchema(PostBaseSchema):
    pub_date: datetime = Field(default_factory=datetime.today, description='Дата и время публикации')
    author_id: int = Field(..., description='Автор публикации')
    is_published: bool | None = Field(None, description='Опубликовано')

class PostUpdateSchema(PostBaseSchema):
    is_published: bool | None = Field(None, description='Опубликовано')


class PostResponseSchema(PostBaseSchema):
    id: int = Field(..., description='ID')
    pub_date: datetime = Field(..., description='Дата и время публикации')
    author: UserResponseSchema = Field(..., description='Автор публикации')
    is_published: bool = Field(..., description='Опубликовано')
    created_at: datetime = Field(..., description='Дата и время создания')
    images: List[ImageSchema] = Field(default_factory=list, description='Изображения поста')