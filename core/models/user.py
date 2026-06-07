from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.api.schemas.user_schemas import UserRole
from core.models.base import Base
from core.models.reservation import Reservation

if TYPE_CHECKING:
    from .reservation import Reservation

class User(Base):
    email: Mapped[str] = mapped_column(unique=True)
    login: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(default=UserRole.USER)

    reservation: Mapped["Reservation"] = relationship(back_populates="user")
