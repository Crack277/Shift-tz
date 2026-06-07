from datetime import datetime
from typing import TYPE_CHECKING


from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .room import Room
    from .time_slot import Time_Slot


class Reservation(Base):
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
    )
    room_id: Mapped[int] = mapped_column(
        ForeignKey("rooms.id"),
    )
    time_slot_id: Mapped[int] = mapped_column(
        ForeignKey("time_slots.id"),
    )

    user: Mapped["User"] = relationship(
        back_populates="reservation",
        foreign_keys=[user_id],
    )
    room: Mapped["Room"] = relationship(
        back_populates="reservation",
        foreign_keys=[room_id],
    )
    time_slot: Mapped["Time_Slot"] = relationship(
        back_populates="reservation",
        foreign_keys=[time_slot_id],
    )