from pydantic import BaseModel, Field
from datetime import datetime


class CommentSchema(BaseModel):
    author: int = Field(..., description='Автор комментария')
    post: int = Field(..., description='Публикация')
    text: str = Field(description='Текст комментария')
    created_at: datetime = Field(
        default=datetime.now(),
        description='Дата и время создания'
    )
