from datetime import datetime
from pydantic import BaseModel, Field, field_validator

class TimeSlotSchema(BaseModel):
    """Базовая схема временного слота"""

    start_time: datetime = Field(
        default=datetime.now().replace(second=0, microsecond=0)
    )
    end_time: datetime = Field(
        default=datetime.now().replace(second=0, microsecond=0)
    )

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def normalize_time(cls, value: datetime) -> datetime:
        if isinstance(value, datetime):
            return value.replace(second=0, microsecond=0)
        return value

    @field_validator("start_time")
    @classmethod
    def not_past(cls, v: datetime) -> datetime:
        if v < datetime.now():
            raise ValueError("Нельзя создавать слоты в прошлом")
        return v

    @field_validator("end_time")
    @classmethod
    def end_after_start(cls, v: datetime, info) -> datetime:
        start = info.data.get("start_time")
        if start and v <= start:
            raise ValueError("Время окончания должно быть позже времени начала")
        return v

class TimeSlotResponse(TimeSlotSchema):
    """Схема ответа с ID слота и комнаты"""

    id: int
    room_id: int


class TimeSlotCreate(TimeSlotSchema):
    """Схема для создания временного слота"""

    pass