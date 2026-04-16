import re
from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, Field, ConfigDict, field_validator
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

    @field_validator("title", mode='after')
    @staticmethod
    def validate_title(title: str) -> str:
        if title is not None and not title.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Заголовок категории не может быть пустым"
            )
        return title


    @field_validator("slug", mode='after')
    @staticmethod
    def validate_slug(slug: str) -> str:
        if slug.startswith('-') or slug.endswith('-'):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Slug не должен начинаться/заканчиваться символом '-'"
            )
        if not re.match(r"^[a-zA-Z0-9_-]+$", slug):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Slug может содержать только латинские буквы, цифры, дефис и '_'"
            )
        return slug


class CategoryUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: Optional[str] = Field(min_length=1, max_length=256, description='Заголовок')
    description: Optional[str] = Field(min_length=1, max_length=2000, description='Описание')
    is_published: Optional[bool] = Field(None, description='Опубликовано')

    @field_validator("title", mode='after')
    @staticmethod
    def validate_title(title: str) -> str:
        if title is not None and not title.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Заголовок категории не может быть пустым"
            )
        return title

class CategoryResponseSchema(CategoryCreateSchema):
    id: int = Field(..., description='ID')
    created_at: datetime = Field(..., description='Дата и время создания')