from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.api.schemas.room_schemas import RoomCreate
from core.api.schemas.time_slot_schemas import TimeSlotCreate
from core.api.services.room_service import RoomService
from core.api.utils import safety
from core.config import settings
from core.database_helper import db_helper
from core.models import User

router = APIRouter(prefix=settings.api.v1.rooms, tags=["ROOMS"])


@router.get("/")
async def get_rooms(session: AsyncSession = Depends(db_helper.session_dependency)):
    """
    Получить список всех комнат.
    Доступно всем авторизованным пользователям.
    """
    service = RoomService(session)
    return await service.get_rooms()


@router.post("/")
async def create_room(
    room_in: RoomCreate,
    current_user: User = Depends(safety.get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Создать новую комнату.
    Только для администратора.
    """
    service = RoomService(session)
    return await service.create_room(
        current_user=current_user, room_in=room_in
    )


@router.delete("/{room_id}/")
async def delete_room(
    room_id: int,
    current_user: User = Depends(safety.get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Удалить комнату по ID.
    Только для администратора.
    """
    service = RoomService(session)
    return await service.delete_room(
        current_user=current_user, room_id=room_id
    )


@router.post("/{room_id}/time-slots/")
async def create_time_slot(
    room_id: int,
    slot_in: TimeSlotCreate,
    current_user: User = Depends(safety.get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Создать временной слот для комнаты.
    Только для администратора.
    """
    service = RoomService(session)
    return await service.create_time_slot(
        current_user=current_user, room_id=room_id, slot_in=slot_in
    )


@router.get("/availability/")
async def get_rooms_availability(
    date: date,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Получить доступность всех комнат на конкретную дату.
    Показывает для каждой комнаты все слоты и их статус (свободен/занят).
    Доступно всем авторизованным пользователям.
    """
    service = RoomService(session)
    return await service.get_rooms_availability(date=date)