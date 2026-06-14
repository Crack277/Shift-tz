from datetime import date as DATE
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .room import Room
    from .time_slot import TimeSlot


class Reservation(Base):
    """Модель бронирования переговорной комнаты"""

    date: Mapped[DATE] = mapped_column(
        Date,
        nullable=False,
        default=DATE.today,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    room_id: Mapped[int] = mapped_column(
        ForeignKey("rooms.id"),
        nullable=False,
    )
    time_slot_id: Mapped[int] = mapped_column(
        ForeignKey("timeslots.id"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="reservation",
        foreign_keys=[user_id],
    )
    room: Mapped["Room"] = relationship(
        back_populates="reservation",
        foreign_keys=[room_id],
    )
    time_slot: Mapped["TimeSlot"] = relationship(
        back_populates="reservation",
        foreign_keys=[time_slot_id],
    )
