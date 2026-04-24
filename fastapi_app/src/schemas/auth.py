from pydantic import Field, BaseModel
from resources.field_description import ACCESS_TOKEN, TOKEN_TYPE


class Token(BaseModel):
    access_token: str = Field(description=ACCESS_TOKEN)
    token_type: str = Field(description=TOKEN_TYPE)