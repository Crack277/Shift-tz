from datetime import date
from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.api.schemas.room_schemas import RoomCreate
from core.api.schemas.time_slot_schemas import TimeSlotCreate
from core.models import Room, Reservation, TimeSlot


class RoomRepository:
    """Репозиторий для операций с комнатами"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_rooms(self) -> List[Room]:
        """Получить список всех комнат"""
        stmt = select(Room).order_by(Room.id)
        result = await self.session.execute(stmt)
        rooms = result.scalars().all()
        return list(rooms)

    async def get_room_by_id(self, room_id: int) -> Room | None:
        """Получить комнату по ID"""
        return await self.session.get(Room, room_id)

    async def create_room(self, room_in: RoomCreate) -> Room:
        """Создать новую комнату"""
        stmt = select(Room).where(Room.name == room_in.name)
        result = await self.session.scalar(stmt)

        if result is None:
            room = Room(**room_in.model_dump())
            self.session.add(room)
            await self.session.commit()
            await self.session.refresh(room)
            return room

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Комната уже существует!"
        )

    async def delete_room(self, room_id: int) -> None:
        """Удалить комнату по ID"""
        room = await self.get_room_by_id(room_id=room_id)
        if room is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Комната не найдена!"
            )

        await self.session.delete(room)
        await self.session.commit()


    async def create_time_slot(self, room_id: int, slot_in: TimeSlotCreate) -> TimeSlot:
        """Создать временной слот для комнаты"""

        room = await self.get_room_by_id(room_id)

        if room is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Комната не найдена!"
            )

        stmt = select(TimeSlot).where(
            TimeSlot.room_id == room_id,
            TimeSlot.start_time < slot_in.end_time,
            TimeSlot.end_time > slot_in.start_time,
        )
        if await self.session.scalar(stmt):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Слот пересекается с существующим"
            )
        
        time_slot = TimeSlot(**slot_in.model_dump(), room_id=room_id)
        self.session.add(time_slot)
        await self.session.commit()
        await self.session.refresh(time_slot)
        return time_slot

    
    async def get_rooms_with_availability(self, date: date) -> List[dict]:
        """
        Получить список комнат с доступностью на конкретную дату.
        Для каждой комнаты показывает все слоты и их статус (свободен/занят).
        """
        rooms = await self.get_rooms()

        stmt = select(Reservation).where(
            Reservation.date == date
        )
        result = await self.session.execute(stmt)

        booked_slots = {
            (r.room_id, r.time_slot_id)
            for r in result.scalars()
        }

        stmt = select(TimeSlot)
        result = await self.session.execute(stmt)
        all_slots = result.scalars().all()

        slots_by_room = {}

        for slot in all_slots:
            slots_by_room.setdefault(
                slot.room_id, []
            ).append(slot)

        result_list = []

        for room in rooms:
            room_slots = slots_by_room.get(room.id, [])

            room_data = {
                "room_id": room.id,
                "room_name": room.name,
                "date": date.isoformat(),
                "slots": [
                    {
                        "time_slot_id": s.id,
                        "start_time": s.start_time.strftime("%H:%M"),
                        "end_time": s.end_time.strftime("%H:%M"),
                        "is_available": (
                            room.id,
                            s.id,
                        ) not in booked_slots,
                    }
                    for s in room_slots
                ],
            }

            result_list.append(room_data)

        return result_list
