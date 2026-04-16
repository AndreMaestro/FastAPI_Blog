import re
from fastapi import HTTPException, status
from pydantic import BaseModel, SecretStr, ConfigDict, field_validator, Field
from datetime import datetime
from typing import Optional


class UserBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username:str = Field(..., max_length=150, description="Имя пользователя")
    email: Optional[str] = Field(None, description="Email")
    first_name: Optional[str] = Field(None, description="Имя")
    last_name: Optional[str] = Field(None, description="Фамилия")
    is_staff: bool = False
    is_active: bool = False
    is_superuser: bool = False

    @field_validator("username", mode='after')
    @staticmethod
    def validate_username(username: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_]+$", username):
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Имя пользователя может содержать только латинские буквы, цифры и '_'"
            )
        if len(username) < 3:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Имя пользователя должно содержать минимум 3 символа"
            )
        return username

    @field_validator("email", mode='after')
    @staticmethod
    def validate_email(email: Optional[str]) -> Optional[str]:
        if email is not None and '@' not in email:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Некорректный формат email"
            )
        return email

    @field_validator("first_name", "last_name", mode='after')
    @staticmethod
    def validate_names(name: Optional[str]) -> Optional[str]:
        if name is not None and not re.match(r"^[a-zA-Zа-яА-ЯёЁ\s\-]+$", name):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Имя и фамилия могут содержать только буквы, дефис и пробел"
            )
        return name


class UserResponseSchema(UserBaseSchema):
    id: int
    last_login: Optional[datetime]
    date_joined: datetime


class UserCreateSchema(UserBaseSchema):
    password: str = Field(..., min_length=8, max_length=128, description="Пароль")

    @field_validator("password", mode='after')
    @staticmethod
    def validate_password(password: str) -> str:
        if len(password) < 8:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Пароль должен содержать минимум 8 символов"
            )
        if not re.search(r"[A-Z]", password):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Пароль должен содержать хотя бы одну заглавную букву"
            )
        if not re.search(r"[a-z]", password):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Пароль должен содержать хотя бы одну строчную букву"
            )
        if not re.search(r"\d", password):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Пароль должен содержать хотя бы одну цифру"
            )
        return password


class UserUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: Optional[str] = Field(None, min_length=3, max_length=150, description="Имя пользователя")
    email: Optional[str] = Field(None, description="Email")
    first_name: Optional[str] = Field(None, description="Имя")
    last_name: Optional[str] = Field(None, description="Фамилия")
    is_staff: Optional[bool] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    password: Optional[str] = Field(None, max_length=128, description="Пароль")

    @field_validator("username", mode='after')
    @staticmethod
    def validate_username(username: Optional[str]) -> Optional[str]:
        if username is not None and not re.match(r"^[a-zA-Z0-9_]+$", username):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Имя пользователя может содержать только латинские буквы, цифры и '_'"
            )
        if username is not None and len(username) < 3:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Имя пользователя должно содержать минимум 3 символа"
            )
        return username

    @field_validator("email", mode='after')
    @staticmethod
    def validate_email(email: Optional[str]) -> Optional[str]:
        if email is not None and '@' not in email:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Некорректный формат email"
            )
        return email

    @field_validator("first_name", "last_name", mode='after')
    @staticmethod
    def validate_names(name: Optional[str]) -> Optional[str]:
        if name is not None and not re.match(r"^[a-zA-Zа-яА-ЯёЁ\s\-]+$", name):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Имя и фамилия могут содержать только буквы, дефис и пробел"
            )
        return name

    @field_validator("password", mode='after')
    @staticmethod
    def validate_password(password: Optional[str]) -> Optional[str]:
        if password is not None and len(password) < 8:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Пароль должен содержать минимум 8 символов"
            )
        if password is not None and not re.search(r"[A-Z]", password):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Пароль должен содержать хотя бы одну заглавную букву"
            )
        if password is not None and not re.search(r"[a-z]", password):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Пароль должен содержать хотя бы одну строчную букву"
            )
        if password is not None and not re.search(r"\d", password):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Пароль должен содержать хотя бы одну цифру"
            )
        return password