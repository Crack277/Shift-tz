from .base import Base

from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .reservation import Reservation
    from .time_slot import Time_Slot

class Room(Base):
    name: Mapped[str] = mapped_column(String(32))

    reservation: Mapped["Reservation"] = relationship(back_populates="room")
    time_slot: Mapped["Time_Slot"] = relationship(back_populates="room")