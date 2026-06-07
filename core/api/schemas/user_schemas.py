from enum import Enum
from pydantic import BaseModel, EmailStr, Field



class UserRole(str, Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"
    USER = "user"


class UserSchemas(BaseModel):
    email: EmailStr
    login: str = Field()
    password: str = Field()
    role: str = Field()