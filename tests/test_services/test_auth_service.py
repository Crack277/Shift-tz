import pytest
from datetime import date
from unittest.mock import AsyncMock, MagicMock, patch

from core.api.services.auth_service import AuthService
from core.api.schemas.user_schemas import UserAuthorize, UserRole
from core.api.schemas.reservation_schemas import ReservationCreate


class TestAuthService:
    """Тесты AuthService"""
    
    @pytest.mark.asyncio
    async def test_login_user_success(self, mock_session, mock_user):
        """Тест успешного входа пользователя"""
        service = AuthService(mock_session)
        service.user_repository.get_user_by_login = AsyncMock(return_value=mock_user)
        
        mock_token = MagicMock()
        mock_token.access_token = "test_token_123"
        
        with patch('core.api.utils.safety.verify_password', return_value=True):
            with patch('core.api.utils.safety.create_access_token', return_value=mock_token):
                user_in = UserAuthorize(login="test@example.com", password="password123")
                
                result = await service.login_user(user_in)
                
                assert result.access_token == "test_token_123"

    @pytest.mark.asyncio
    async def test_login_user_wrong_password(self, mock_session, mock_user):
        """Тест входа с неверным паролем"""
        service = AuthService(mock_session)
        service.user_repository.get_user_by_login = AsyncMock(return_value=mock_user)
        
        with patch('core.api.utils.safety.verify_password', return_value=False):
            user_in = UserAuthorize(login="test@example.com", password="wrongwrong")
            
            with pytest.raises(Exception) as exc_info:
                await service.login_user(user_in)
            
            assert "Неверный логин или пароль" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_create_reservation_success(self, mock_session, mock_user, mock_room, mock_time_slot):
        """Тест успешного создания бронирования"""
        service = AuthService(mock_session)
        service.room_repository.get_room_by_id = AsyncMock(return_value=mock_room)
        service.user_repository.get_time_slot_by_id = AsyncMock(return_value=mock_time_slot)
        service.user_repository.create_reservation = AsyncMock(return_value=True)
        
        reservation_in = ReservationCreate(
            date=date(2026, 6, 15),
            room_id=1,
            time_slot_id=1,
        )
        
        result = await service.create_reservation(mock_user, reservation_in)
        
        assert result is True

    @pytest.mark.asyncio
    async def test_create_reservation_room_not_found(self, mock_session, mock_user):
        """Тест создания бронирования в несуществующей комнате"""
        service = AuthService(mock_session)
        service.room_repository.get_room_by_id = AsyncMock(return_value=None)
        
        reservation_in = ReservationCreate(
            date=date(2026, 6, 15),
            room_id=999,
            time_slot_id=1,
        )
        
        with pytest.raises(Exception) as exc_info:
            await service.create_reservation(mock_user, reservation_in)
        
        assert "Комната не найдена" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_reservations_by_day_as_employee(self, mock_session, mock_user, mock_reservation):
        """Тест получения бронирований сотрудником (только свои)"""
        service = AuthService(mock_session)
        service.user_repository.get_reservations_by_day = AsyncMock(return_value=[mock_reservation])
        
        mock_user.role = UserRole.EMPLOYEE
        mock_reservation.user_id = 1
        mock_user.id = 1
        
        result = await service.get_reservations_by_day(date(2026, 6, 15), mock_user)
        
        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_get_reservations_by_day_as_admin(self, mock_session, mock_admin, mock_reservation):
        """Тест получения бронирований администратором (все)"""
        service = AuthService(mock_session)
        service.user_repository.get_reservations_by_day = AsyncMock(return_value=[mock_reservation])
        
        mock_admin.role = UserRole.ADMIN
        
        result = await service.get_reservations_by_day(date(2026, 6, 15), mock_admin)
        
        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_delete_reservation_as_owner(self, mock_session, mock_user, mock_reservation):
        """Тест удаления бронирования владельцем"""
        service = AuthService(mock_session)
        service.user_repository.get_reservation_by_id = AsyncMock(return_value=mock_reservation)
        service.user_repository.delete_reservation = AsyncMock()
        
        mock_reservation.user_id = 1
        mock_user.id = 1
        mock_user.role = UserRole.EMPLOYEE
        
        await service.delete_reservation(1, mock_user)
        
        service.user_repository.delete_reservation.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_reservation_as_admin(self, mock_session, mock_admin, mock_reservation):
        """Тест удаления чужого бронирования администратором"""
        service = AuthService(mock_session)
        service.user_repository.get_reservation_by_id = AsyncMock(return_value=mock_reservation)
        service.user_repository.delete_reservation = AsyncMock()
        
        mock_admin.role = UserRole.ADMIN
        mock_reservation.user_id = 2
        
        await service.delete_reservation(1, mock_admin)
        
        service.user_repository.delete_reservation.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_reservation_not_owner(self, mock_session, mock_user, mock_reservation):
        """Тест удаления чужого бронирования обычным пользователем"""
        service = AuthService(mock_session)
        service.user_repository.get_reservation_by_id = AsyncMock(return_value=mock_reservation)
        
        mock_user.role = UserRole.EMPLOYEE
        mock_reservation.user_id = 2
        mock_user.id = 1
        
        with pytest.raises(Exception) as exc_info:
            await service.delete_reservation(1, mock_user)
        
        assert "Отказано в доступе" in str(exc_info.value)