import pytest
from datetime import date
from unittest.mock import AsyncMock, MagicMock

from core.models import TimeSlot


class TestUserRepository:
    """Тесты UserRepository"""
    
    @pytest.mark.asyncio
    async def test_get_user_by_login_success(self, user_repository, mock_session, mock_user):
        """Тест успешного получения пользователя по логину"""
        mock_session.scalar = AsyncMock(return_value=mock_user)
        
        result = await user_repository.get_user_by_login("test@example.com")
        
        assert result == mock_user

    @pytest.mark.asyncio
    async def test_get_user_by_login_not_found(self, user_repository, mock_session):
        """Тест получения несуществующего пользователя"""
        mock_session.scalar = AsyncMock(return_value=None)
        
        result = await user_repository.get_user_by_login("nonexistent@example.com")
        
        assert result is None

    @pytest.mark.asyncio
    async def test_create_user_already_exists(self, user_repository, mock_session, mock_user_create, mock_user):
        """Тест создания уже существующего пользователя"""
        mock_session.scalar = AsyncMock(return_value=mock_user)
        
        with pytest.raises(Exception) as exc_info:
            await user_repository.create_user(mock_user_create)
        
        assert "уже зарегистрирован" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_time_slot_by_id_success(self, user_repository, mock_session, mock_time_slot):
        """Тест успешного получения временного слота по ID"""
        mock_session.get = AsyncMock(return_value=mock_time_slot)
        
        result = await user_repository.get_time_slot_by_id(1)
        
        assert result == mock_time_slot
        mock_session.get.assert_called_once_with(TimeSlot, 1)

    @pytest.mark.asyncio
    async def test_get_time_slot_by_id_not_found(self, user_repository, mock_session):
        """Тест получения несуществующего слота"""
        mock_session.get = AsyncMock(return_value=None)
        
        with pytest.raises(Exception) as exc_info:
            await user_repository.get_time_slot_by_id(999)
        
        assert "Слот не найден" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_create_reservation_success(self, user_repository, mock_session):
        """Тест успешного создания бронирования"""
        mock_session.scalar = AsyncMock(return_value=None)
        mock_session.add = MagicMock()
        mock_session.commit = AsyncMock()
        mock_session.refresh = AsyncMock()
        
        result = await user_repository.create_reservation(
            date=date(2026, 6, 15),
            user_id=1,
            room_id=1,
            time_slot_id=1,
        )
        
        assert result is not None

    @pytest.mark.asyncio
    async def test_create_reservation_double_booking(self, user_repository, mock_session):
        """Тест создания двойного бронирования"""
        mock_session.scalar = AsyncMock(return_value=True)
        
        with pytest.raises(Exception) as exc_info:
            await user_repository.create_reservation(
                date=date(2026, 6, 15),
                user_id=1,
                room_id=1,
                time_slot_id=1,
            )
        
        assert "Время уже занято" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_delete_reservation(self, user_repository, mock_session, mock_reservation):
        """Тест удаления бронирования"""
        mock_session.delete = AsyncMock()
        mock_session.commit = AsyncMock()
        
        await user_repository.delete_reservation(mock_reservation)
        
        mock_session.delete.assert_called_once_with(mock_reservation)