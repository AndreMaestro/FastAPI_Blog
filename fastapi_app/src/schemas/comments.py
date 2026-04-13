from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class CommentCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    author_id: int = Field(..., description='Автор комментария')
    post_id: int = Field(..., description='Публикация')
    text: str = Field(min_length=1, max_length=256, description='Текст комментария')


class CommentUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    text: str = Field(min_length=1, max_length=256, description='Текст комментария')


class CommentResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description='ID')
    author_id: int = Field(..., description='Автор комментария')
    post_id: int = Field(..., description='Публикация')
    text: str = Field(min_length=1, max_length=256, description='Текст комментария')
    created_at: datetime = Field(
        default=datetime.now(),
        description='Дата и время создания'
    )
