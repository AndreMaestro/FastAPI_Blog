import re
from fastapi import HTTPException, status
from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime


class LocationBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(min_length=1, max_length=256, description='Название места')
    is_published: bool | None = Field(None, description='Опубликовано')


    @field_validator("name", mode='after')
    @staticmethod
    def validate_name(name: str) -> str:
        if not name.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Название локации не должно состоять только из пробелов"
            )
        if not re.match(r"^[a-zA-Zа-яА-ЯёЁ0-9\s\-]+$", name):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Название локации может содержать только буквы, цифры, дефис и пробел"
            )
        return name


class LocationResponseSchema(LocationBaseSchema):
    id: int = Field(..., description='ID')
    created_at: datetime = Field(..., description='Дата и время создания')


class LocationCreateUpdateSchema(LocationBaseSchema):
    pass