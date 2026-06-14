from datetime import date
from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.api.schemas.user_schemas import UserCreate
from core.api.utils import safety
from core.models import User, TimeSlot, Reservation


class UserRepository:
    """Репозиторий для операций с пользователями"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_users(self) -> List[User]:
        """Получить список всех пользователей"""
        stmt = select(User).order_by(User.id)
        result = await self.session.execute(stmt)
        users = result.scalars().all()
        return list(users)

    async def get_user_by_id(self, user_id: int) -> User:
        """Получить пользователя по ID"""
        return await self.session.get(User, user_id)

    async def get_user_by_login(self, login: str) -> User:
        """Получить пользователя по логину"""
        stmt = select(User).where(User.login == login)
        result = await self.session.scalar(stmt)

        return result

    async def create_user(self, user_in: UserCreate) -> User:
        """Создать нового пользователя"""
        user = await self.get_user_by_login(login=user_in.login)

        if user is None:
            if user_in.password == user_in.repeat_password:
                hashed_password = safety.get_hashed_password(user_in.password)
                user = User(
                    login=user_in.login,
                    password=hashed_password,
                    role=user_in.role,
                )
                self.session.add(user)
                await self.session.commit()
                await self.session.refresh(user)
                return user

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пароли должны совпадать!",
            )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Данный пользователь уже зарегистрирован!",
        )
    
    async def get_time_slot_by_id(self, time_slot_id: int) -> TimeSlot:
        """Получить временной слот по ID"""
        time_slot = await self.session.get(TimeSlot, time_slot_id)

        if time_slot is not None:
            return time_slot
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Слот не найден!"
        )

    async def create_reservation(
        self, date: date, user_id: int, room_id: int, time_slot_id: int
    ) -> Reservation:
        """Создать бронирование"""
        stmt = select(Reservation).where(
            Reservation.date == date,
            Reservation.room_id == room_id,
            Reservation.time_slot_id == time_slot_id,
        )
        existing = await self.session.scalar(stmt)

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Время уже занято!"
            )

        reservation = Reservation(
            date=date,
            user_id=user_id,
            room_id=room_id,
            time_slot_id=time_slot_id,
        )

        self.session.add(reservation)
        await self.session.commit()
        await self.session.refresh(reservation)
        return reservation

    async def get_reservations_by_day(self, date: date) -> List[Reservation]:
        """Получить все бронирования на конкретную дату"""
        stmt = (
            select(Reservation)
            .where(Reservation.date == date)
            .order_by(Reservation.id)
        )
        result = await self.session.execute(stmt)
        reservations = result.scalars().all()
        return list(reservations)

    async def get_reservation_by_id(self, reservation_id: int) -> Reservation:
        """Получить бронирование по ID"""
        stmt = select(Reservation).where(Reservation.id == reservation_id)
        reservation = await self.session.scalar(stmt)

        return reservation

    async def delete_reservation(self, reservation: Reservation) -> None:
        """Удалить бронирование"""
        await self.session.delete(reservation)
        await self.session.commit()
