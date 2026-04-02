from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class LocationResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description='ID')
    name: str = Field(..., max_length=256, description='Название места')
    is_published: bool | None = Field(None, description='Опубликовано')
    created_at: datetime = Field(..., description='Дата и время создания')


class LocationCreateUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(..., max_length=256, description='Название места')
    is_published: bool | None = Field(None, description='Опубликовано')
