from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .reservation import Reservation
    from .time_slot import TimeSlot


class Room(Base):
    """Модель переговорной комнаты"""

    name: Mapped[str] = mapped_column(String(32))

    reservation: Mapped[List["Reservation"]] = relationship(back_populates="room")
    time_slot: Mapped[List["TimeSlot"]] = relationship(back_populates="room")
