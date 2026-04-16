from fastapi import HTTPException, status
from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime


class CommentBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    text: str = Field(min_length=1, max_length=256, description='Текст комментария')

    @field_validator("text", mode='after')
    @staticmethod
    def validate(text: str) -> str:
        if not text.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Комментарий не может быть пустым"
            )
        return text

class CommentCreateSchema(CommentBaseSchema):
    author_id: int = Field(..., description='Автор комментария')
    post_id: int = Field(..., description='Публикация')


class CommentUpdateSchema(CommentBaseSchema):
    pass


class CommentResponseSchema(CommentBaseSchema):
    id: int = Field(..., description='ID')
    author_id: int = Field(..., description='Автор комментария')
    post_id: int = Field(..., description='Публикация')
    created_at: datetime = Field(
        default=datetime.now,
        description='Дата и время создания'
    )
