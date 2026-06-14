from datetime import date
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.api.repositories.room_repository import RoomRepository
from core.api.schemas.room_schemas import RoomCreate
from core.api.schemas.time_slot_schemas import TimeSlotCreate
from core.api.schemas.user_schemas import UserRole
from core.models import Room, TimeSlot, User


class RoomService:
    """Сервис для управления комнатами и слотами"""

    def __init__(self, session: AsyncSession):
        self.room_repository = RoomRepository(session)
        self.session = session

    async def get_rooms(self) -> List[Room]:
        """Получить список всех комнат (доступно всем)"""
        return await self.room_repository.get_rooms()

    async def create_room(self, current_user: User, room_in: RoomCreate) -> Room:
        """Создать новую комнату (только для администратора)"""
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Только администратор может создавать комнаты"
            )
        return await self.room_repository.create_room(room_in=room_in)
    
    async def create_time_slot(self, current_user: User, room_id: int, slot_in: TimeSlotCreate) -> TimeSlot:
        """Создать временной слот (только для администратора)"""
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Только для администратора"
            )
        
        return await self.room_repository.create_time_slot(
            room_id=room_id, slot_in=slot_in
        )

    async def delete_room(self, current_user: User, room_id: int) -> None:
        """Удалить комнату (только для администратора)"""
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Только администратор может удалять комнаты"
            )

        return await self.room_repository.delete_room(room_id=room_id)

    async def get_rooms_availability(self, date: date) -> List[dict]:
        """Получить доступность всех комнат на дату (доступно всем)"""
        return await self.room_repository.get_rooms_with_availability(date=date)