from enum import Enum
from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    """Роли пользователей"""
    
    ADMIN: str = "admin"
    EMPLOYEE: str = "employee"


class UserSchema(BaseModel):
    """Базовая схема пользователя"""

    login: EmailStr
    password: str = Field(min_length=8, max_length=32)


class UserCreate(UserSchema):
    """Схема для создания нового пользователя"""

    repeat_password: str = Field(min_length=8, max_length=32)
    role: UserRole = Field(default=UserRole.EMPLOYEE)


class UserAuthorize(UserSchema):
    """Схема для авторизации (логин + пароль)"""

    pass


class PrintToken(BaseModel):
    """Схема ответа с JWT токеном"""

    access_token: str
    type: str = "Bearer"
