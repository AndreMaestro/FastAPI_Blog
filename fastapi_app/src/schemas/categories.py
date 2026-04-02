from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class CategoryCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str = Field(..., max_length=256, description='Заголовок')
    description: str = Field(..., description='Описание')
    is_published: bool | None = Field(None, description='Опубликовано')
    slug: str = Field(
        ...,
        pattern=r'^[a-zA-Z0-9_-]+$',
        description='Идентификатор, разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )


class CategoryUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str = Field(..., max_length=256, description='Заголовок')
    description: str = Field(..., description='Описание')
    is_published: bool | None = Field(None, description='Опубликовано')


class CategoryResponseSchema(BaseModel):
    id: int = Field(..., description='ID')
    model_config = ConfigDict(from_attributes=True)
    title: str = Field(..., max_length=256, description='Заголовок')
    description: str = Field(..., description='Описание')
    slug: str = Field(
        ...,
        pattern=r'^[a-zA-Z0-9_-]+$',
        description='Идентификатор, разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )
    created_at: datetime = Field(..., description='Дата и время создания')