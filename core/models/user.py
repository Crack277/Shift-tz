from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLAlchemy_Enum

from core.api.schemas.user_schemas import UserRole
from core.models import Base


if TYPE_CHECKING:
    from .reservation import Reservation


class User(Base):
    """Модель пользователя системы"""
    
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SQLAlchemy_Enum(UserRole),
        default=UserRole.EMPLOYEE,
        nullable=False,
    )

    reservation: Mapped[List["Reservation"]] = relationship(back_populates="user")
