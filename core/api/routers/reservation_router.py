from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.api.schemas.reservation_schemas import ReservationCreate
from core.api.services.auth_service import AuthService
from core.api.utils import safety
from core.config import settings
from core.database_helper import db_helper
from core.models import User

router = APIRouter(prefix=settings.api.v1.reservations, tags=["RESERVATIONS"])


@router.get("/")
async def get_reservations_by_day(
    date: date,
    current_user: User = Depends(safety.get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Получить все бронирования на указанную дату.
    - Сотрудник видит только свои бронирования
    - Администратор видит все бронирования
    """
    service = AuthService(session)
    return await service.get_reservations_by_day(
        current_user=current_user, date=date
    )


@router.post("/")
async def create_reservation(
    reservation_in: ReservationCreate,
    current_user: User = Depends(safety.get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Создать новое бронирование.
    Доступно всем авторизованным пользователям.
    """
    service = AuthService(session)
    return await service.create_reservation(
        current_user=current_user, reservation_in=reservation_in
    )


@router.delete("/{reservation_id}/")
async def delete_reservation(
    reservation_id: int,
    current_user: User = Depends(safety.get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Отменить бронирование.
    - Сотрудник может отменить только свои бронирования
    - Администратор может отменить любые бронирования
    """
    service = AuthService(session)
    return await service.delete_reservation(
        current_user=current_user, reservation_id=reservation_id
    )
