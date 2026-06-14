from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .room import Room
    from .reservation import Reservation


class TimeSlot(Base):
    """Модель временного слота (например, 09:00-11:00)"""

    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    room_id: Mapped[int] = mapped_column(
        ForeignKey("rooms.id"),
    )

    room: Mapped["Room"] = relationship(back_populates="time_slot")
    reservation: Mapped["Reservation"] = relationship(back_populates="time_slot")
