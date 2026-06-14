from pydantic import BaseModel, Field


class RoomSchema(BaseModel):
    """Базовая схема комнаты"""

    name: str = Field(max_length=32)


class RoomCreate(RoomSchema):
    """Схема для создания комнаты"""
    
    pass
