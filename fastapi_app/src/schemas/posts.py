from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

from .categories import CategoryResponseSchema
from .locations import LocationResponseSchema
from .users import UserSchema


class PostBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str = Field(..., max_length=256, description='Заголовок')
    text: str = Field(..., description='Текст')
    location_id: int | None = Field(None, description='Местоположение')
    category_id: int | None = Field(None, description='Категория')
    image: str | None = Field(None, description="Image")

class PostCreateSchema(PostBaseSchema):
    pub_date: datetime = Field(..., description='Дата и время публикации')
    author_id: int = Field(..., description='Автор публикации')
    is_published: bool | None = Field(None, description='Опубликовано')

class PostUpdateSchema(PostBaseSchema):
    is_published: bool | None = Field(None, description='Опубликовано')

class PostResponseSchema(PostBaseSchema):
    id: int = Field(..., description='ID')
    pub_date: datetime = Field(..., description='Дата и время публикации')
    author: UserSchema = Field(..., description='Автор публикации')
    is_published: bool = Field(..., description='Опубликовано')
    created_at: datetime = Field(..., description='Дата и время создания')