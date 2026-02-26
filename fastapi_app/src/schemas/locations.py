from pydantic import BaseModel, Field


class LocationSchema(BaseModel):
    name: str = Field(..., max_length=256, description='Название места')
