from pydantic import BaseModel, SecretStr, ConfigDict
from datetime import datetime
from typing import Optional

class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    login:str
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    password: SecretStr
    is_staff: bool
    is_active: bool
    is_superuser: bool
    last_login: Optional[datetime]
    date_joined: datetime