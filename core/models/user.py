from sqlalchemy.orm import Mapped, mapped_column

from core.api.schemas.user_schemas import UserRole
from core.models.base import Base


class User(Base):
    email: Mapped[str] = mapped_column(unique=True)
    login: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(default=UserRole.EMPLOYEE)