from unittest.mock import AsyncMock, MagicMock
from datetime import date, datetime

import pytest
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from core.api.repositories.user_repository import UserRepository
from core.api.repositories.room_repository import RoomRepository
from core.api.schemas.user_schemas import UserRole


@pytest.fixture
def mock_session():
    """Фикстура для мок-сессии SQLAlchemy"""
    session = AsyncMock(spec=AsyncSession)
    return session


@pytest.fixture
def mock_credentials():
    """Фикстура для мок-credentials HTTPBearer"""
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials="valid_token")


@pytest.fixture
def user_repository(mock_session):
    """Фикстура для репозитория с мок-сессией"""
    return UserRepository(mock_session)


@pytest.fixture
def room_repository(mock_session):
    """Фикстура для репозитория комнат с мок-сессией"""
    return RoomRepository(mock_session)


@pytest.fixture
def mock_user():
    """Фикстура для тестового пользователя (сотрудник)"""
    user = MagicMock()
    user.id = 1
    user.login = "test@example.com"
    user.password = "hashed_secret123"
    user.role = UserRole.EMPLOYEE
    return user


@pytest.fixture
def mock_admin():
    """Фикстура для тестового администратора"""
    admin = MagicMock()
    admin.id = 2
    admin.login = "admin@example.com"
    admin.password = "hashed_admin123"
    admin.role = UserRole.ADMIN
    return admin


@pytest.fixture
def mock_room():
    """Фикстура для тестовой комнаты"""
    room = MagicMock()
    room.id = 1
    room.name = "Переговорная А"
    return room


@pytest.fixture
def mock_time_slot():
    """Фикстура для тестового временного слота"""
    time_slot = MagicMock()
    time_slot.id = 1
    time_slot.start_time = datetime(2026, 6, 15, 9, 0, 0)
    time_slot.end_time = datetime(2026, 6, 15, 11, 0, 0)
    time_slot.room_id = 1
    return time_slot


@pytest.fixture
def mock_reservation():
    """Фикстура для тестового бронирования"""
    reservation = MagicMock()
    reservation.id = 1
    reservation.date = date(2026, 6, 15)
    reservation.user_id = 1
    reservation.room_id = 1
    reservation.time_slot_id = 1
    return reservation


@pytest.fixture
def mock_reservation_create():
    """Фикстура для данных создания бронирования"""
    from core.api.schemas.reservation_schemas import ReservationCreate
    
    return ReservationCreate(
        date=date(2026, 6, 15),
        room_id=1,
        time_slot_id=1,
    )


@pytest.fixture
def mock_room_create():
    """Фикстура для данных создания комнаты"""
    from core.api.schemas.room_schemas import RoomCreate
    
    return RoomCreate(name="Новая комната")


@pytest.fixture
def mock_time_slot_create():
    """Фикстура для данных создания временного слота"""
    from core.api.schemas.time_slot_schemas import TimeSlotCreate
    
    return TimeSlotCreate(
        start_time=datetime(2026, 6, 15, 14, 0, 0),
        end_time=datetime(2026, 6, 15, 16, 0, 0),
    )


@pytest.fixture
def mock_user_create():
    """Фикстура для данных создания пользователя"""
    from core.api.schemas.user_schemas import UserCreate
    
    return UserCreate(
        login="newuser@example.com",
        password="password123",
        repeat_password="password123",
        role=UserRole.EMPLOYEE,
    )


@pytest.fixture
def mock_user_authorize():
    """Фикстура для данных авторизации"""
    from core.api.schemas.user_schemas import UserAuthorize
    
    return UserAuthorize(
        login="test@example.com",
        password="password123",
    )


@pytest.fixture
def mock_payload():
    """Фикстура для мок-payload JWT токена"""
    return {
        "user_id": 1,
        "login": "test@example.com",
        "exp": 9999999999,
        "created_at": 1234567890,
    }