from pydantic import BaseModel, Field
from datetime import datetime

from .locations import LocationSchema
from .categories import CategorySchema


class PostCreateSchema(BaseModel):
    title: str = Field(..., max_length=256, description='Заголовок')
    text: str = Field(..., description='Текст')
    pub_date: datetime = Field(..., description='Дата и время публикации')
    author: int = Field(..., description='Автор публикации')
    location: LocationSchema | None = Field(None, description='Местоположение')
    category: CategorySchema | None = Field(None, description='Категория')
    # image
    is_published: bool = Field(default=True, description='Опубликовано')
    created_at: datetime = Field(
        default=datetime.now(),
        description='Дата и время создания'
    )


class PostUpdateSchema(BaseModel):
    title: str = Field(..., max_length=256, description='Заголовок')
    text: str = Field(..., description='Текст')
    location: LocationSchema | None = Field(None, description='Местоположение')
    category: CategorySchema | None = Field(None, description='Категория')
    is_published: bool = Field(default=True, description='Опубликовано')


class PostResponseSchema(BaseModel):
    id: int = Field(..., description='ID')
    title: str = Field(..., max_length=256, description='Заголовок')
    text: str = Field(..., description='Текст')
    pub_date: datetime = Field(..., description='Дата и время публикации')
    author: int = Field(..., description='Автор публикации')
    location: LocationSchema | None = Field(None, description='Местоположение')
    category: CategorySchema | None = Field(None, description='Категория')
    # image
    is_published: bool = Field(default=True, description='Опубликовано')
