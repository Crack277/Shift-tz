from datetime import date as Date

from pydantic import BaseModel, Field


class ReservationSchema(BaseModel):
    """Базовая схема бронирования"""

    date: Date = Field(default_factory=Date.today)
    room_id: int = 1
    time_slot_id: int = 1

class ReservationCreate(ReservationSchema):
    """Схема для создания бронирования"""

    pass
