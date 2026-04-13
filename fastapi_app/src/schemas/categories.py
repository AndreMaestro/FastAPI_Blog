from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class CategoryCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str = Field(min_length=1, max_length=256, description='Заголовок')
    description: str = Field(min_length=1, max_length=2000, description='Описание')
    is_published: bool | None = Field(None, description='Опубликовано')
    slug: str = Field(
        min_length=1,
        max_length=50,
        pattern=r'^[a-zA-Z0-9_-]+$',
        description='Идентификатор, разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )


class CategoryUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str = Field(min_length=1, max_length=256, description='Заголовок')
    description: str = Field(min_length=1, max_length=2000, description='Описание')
    is_published: bool | None = Field(None, description='Опубликовано')


class CategoryResponseSchema(BaseModel):
    id: int = Field(..., description='ID')
    model_config = ConfigDict(from_attributes=True)
    title: str = Field(min_length=1, max_length=256, description='Заголовок')
    description: str = Field(min_length=1, max_length=2000, description='Описание')
    slug: str = Field(
        min_length=1,
        max_length=50,
        pattern=r'^[a-zA-Z0-9_-]+$',
        description='Идентификатор, разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )
    created_at: datetime = Field(..., description='Дата и время создания')
    is_published: bool | None = Field(None, description='Опубликовано')