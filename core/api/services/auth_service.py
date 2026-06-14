from datetime import date
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.api.repositories.room_repository import RoomRepository
from core.api.repositories.user_repository import UserRepository
from core.api.schemas.reservation_schemas import ReservationCreate
from core.api.schemas.user_schemas import PrintToken, UserAuthorize
from core.api.utils import safety
from core.models import User, Reservation


class AuthService:
    """Сервис для аутентификации и бронирований"""

    def __init__(self, session: AsyncSession):
        self.user_repository = UserRepository(session)
        self.room_repository = RoomRepository(session)
        self.session = session

    async def login_user(self, user_in: UserAuthorize) -> PrintToken:
        """Аутентификация пользователя и выдача JWT токена"""
        user = await self.user_repository.get_user_by_login(login=user_in.login)

        if not user or not safety.verify_password(user_in.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный логин или пароль!",
            )

        access_token = safety.create_access_token(user=user)
        return access_token

    async def create_reservation(
        self, current_user: User, reservation_in: ReservationCreate
    ) -> Reservation:
        """Создание бронирования"""
        room = await self.room_repository.get_room_by_id(room_id=reservation_in.room_id)
        if room is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Комната не найдена!"
            )

        time_slot = await self.user_repository.get_time_slot_by_id(reservation_in.time_slot_id)

        if time_slot.room_id != reservation_in.room_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Слот не принадлежит выбранной комнате!"
            )

        return await self.user_repository.create_reservation(
            date=reservation_in.date,
            user_id=current_user.id,
            room_id=time_slot.room_id,
            time_slot_id=reservation_in.time_slot_id,
        )

    async def get_reservations_by_day(self, date: date, current_user: User) -> List[dict]:
        """
        Получить бронирования на дату.
        Сотрудник видит только свои бронирования,
        администратор видит все.
        """
        reservations = await self.user_repository.get_reservations_by_day(date=date)

        if current_user.role != "admin":
            reservations = [r for r in reservations if r.user_id == current_user.id]

        return reservations

    async def delete_reservation(self, reservation_id: int, current_user: User) -> None:
        """
        Отмена бронирования.
        Сотрудник может отменить только свои бронирования,
        администратор может отменить любые.
        """
        reservation = await self.user_repository.get_reservation_by_id(reservation_id)
        
        if reservation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Бронирование не найдено!"
            )
        
        if current_user.role != "admin" and reservation.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Отказано в доступе!"
            )
        
        return await self.user_repository.delete_reservation(reservation=reservation)
        

