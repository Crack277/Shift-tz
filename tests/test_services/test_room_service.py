import pytest
from datetime import date
from unittest.mock import AsyncMock

from core.api.services.room_service import RoomService
from core.api.schemas.user_schemas import UserRole


class TestRoomService:
    """Тесты RoomService"""
    
    @pytest.mark.asyncio
    async def test_get_rooms_success(self, mock_session, mock_room):
        """Тест успешного получения списка комнат"""
        service = RoomService(mock_session)
        service.room_repository.get_rooms = AsyncMock(return_value=[mock_room])
        
        result = await service.get_rooms()
        
        assert len(result) == 1
        assert result[0] == mock_room

    @pytest.mark.asyncio
    async def test_create_room_as_admin(self, mock_session, mock_admin, mock_room_create, mock_room):
        """Тест создания комнаты администратором"""
        service = RoomService(mock_session)
        service.room_repository.create_room = AsyncMock(return_value=mock_room)
        
        mock_admin.role = UserRole.ADMIN
        
        result = await service.create_room(mock_admin, mock_room_create)
        
        assert result == mock_room

    @pytest.mark.asyncio
    async def test_create_room_as_employee(self, mock_session, mock_user, mock_room_create):
        """Тест создания комнаты сотрудником (должно быть запрещено)"""
        service = RoomService(mock_session)
        
        mock_user.role = UserRole.EMPLOYEE
        
        with pytest.raises(Exception) as exc_info:
            await service.create_room(mock_user, mock_room_create)
        
        assert "Только администратор может создавать комнаты" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_delete_room_as_admin(self, mock_session, mock_admin):
        """Тест удаления комнаты администратором"""
        service = RoomService(mock_session)
        service.room_repository.delete_room = AsyncMock()
        
        mock_admin.role = UserRole.ADMIN
        
        await service.delete_room(mock_admin, 1)
        
        service.room_repository.delete_room.assert_called_once_with(room_id=1)

    @pytest.mark.asyncio
    async def test_delete_room_as_employee(self, mock_session, mock_user):
        """Тест удаления комнаты сотрудником (должно быть запрещено)"""
        service = RoomService(mock_session)
        
        mock_user.role = UserRole.EMPLOYEE
        
        with pytest.raises(Exception) as exc_info:
            await service.delete_room(mock_user, 1)
        
        assert "Только администратор" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_create_time_slot_as_admin(self, mock_session, mock_admin, mock_time_slot_create, mock_time_slot):
        """Тест создания временного слота администратором"""
        service = RoomService(mock_session)
        service.room_repository.create_time_slot = AsyncMock(return_value=mock_time_slot)
        
        mock_admin.role = UserRole.ADMIN
        
        result = await service.create_time_slot(mock_admin, 1, mock_time_slot_create)
        
        assert result == mock_time_slot

    @pytest.mark.asyncio
    async def test_create_time_slot_as_employee(self, mock_session, mock_user, mock_time_slot_create):
        """Тест создания временного слота сотрудником (должно быть запрещено)"""
        service = RoomService(mock_session)
        
        mock_user.role = UserRole.EMPLOYEE
        
        with pytest.raises(Exception) as exc_info:
            await service.create_time_slot(mock_user, 1, mock_time_slot_create)
        
        assert "Только для администратора" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_rooms_availability(self, mock_session):
        """Тест получения доступности комнат"""
        service = RoomService(mock_session)
        expected_result = [{"room_id": 1, "slots": []}]
        service.room_repository.get_rooms_with_availability = AsyncMock(return_value=expected_result)
        
        result = await service.get_rooms_availability(date(2026, 6, 15))
        
        assert result == expected_result