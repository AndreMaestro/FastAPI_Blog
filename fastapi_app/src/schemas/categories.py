from pydantic import BaseModel, Field


class CategorySchema(BaseModel):
    title: str = Field(..., max_length=256, description='Заголовок')
    description: str = Field(..., description='Описание')
    slug: str = Field(
        ...,
        pattern=r'^[a-zA-Z0-9_-]+$',
        description='Идентификатор, разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )
