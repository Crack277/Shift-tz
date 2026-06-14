import pytest
from unittest.mock import AsyncMock, MagicMock

from core.models import Room


class TestRoomRepository:
    """Тесты RoomRepository"""
    
    @pytest.mark.asyncio
    async def test_get_rooms_success(self, room_repository, mock_session, mock_room):
        """Тест успешного получения списка комнат"""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_room]
        mock_session.execute = AsyncMock(return_value=mock_result)
        
        result = await room_repository.get_rooms()
        
        assert len(result) == 1
        assert result[0] == mock_room

    @pytest.mark.asyncio
    async def test_get_room_by_id_success(self, room_repository, mock_session, mock_room):
        """Тест успешного получения комнаты по ID"""
        mock_session.get = AsyncMock(return_value=mock_room)
        
        result = await room_repository.get_room_by_id(1)
        
        assert result == mock_room
        mock_session.get.assert_called_once_with(Room, 1)

    @pytest.mark.asyncio
    async def test_create_room_success(self, room_repository, mock_session, mock_room_create):
        """Тест успешного создания комнаты"""
        mock_session.scalar = AsyncMock(return_value=None)
        mock_session.add = MagicMock()
        mock_session.commit = AsyncMock()
        mock_session.refresh = AsyncMock()
        
        result = await room_repository.create_room(mock_room_create)
        
        assert result is not None

    @pytest.mark.asyncio
    async def test_create_room_duplicate(self, room_repository, mock_session, mock_room_create):
        """Тест создания комнаты с дублирующимся именем"""
        mock_session.scalar = AsyncMock(return_value=True)
        
        with pytest.raises(Exception) as exc_info:
            await room_repository.create_room(mock_room_create)
        
        assert "уже существует" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_delete_room_success(self, room_repository, mock_session, mock_room):
        """Тест успешного удаления комнаты"""
        mock_session.get = AsyncMock(return_value=mock_room)
        mock_session.delete = AsyncMock()
        mock_session.commit = AsyncMock()
        
        await room_repository.delete_room(1)
        
        mock_session.delete.assert_called_once_with(mock_room)

    @pytest.mark.asyncio
    async def test_delete_room_not_found(self, room_repository, mock_session):
        """Тест удаления несуществующей комнаты"""
        mock_session.get = AsyncMock(return_value=None)
        
        with pytest.raises(Exception) as exc_info:
            await room_repository.delete_room(999)
        
        assert "Комната не найдена" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_create_time_slot_success(self, room_repository, mock_session, mock_time_slot_create):
        """Тест успешного создания временного слота"""
        mock_session.scalar = AsyncMock(return_value=None)
        mock_session.add = MagicMock()
        mock_session.commit = AsyncMock()
        mock_session.refresh = AsyncMock()
        
        result = await room_repository.create_time_slot(1, mock_time_slot_create)
        
        assert result is not None

    @pytest.mark.asyncio
    async def test_create_time_slot_overlap(self, room_repository, mock_session, mock_time_slot_create):
        """Тест создания пересекающегося слота"""
        mock_session.scalar = AsyncMock(return_value=True)
        
        with pytest.raises(Exception) as exc_info:
            await room_repository.create_time_slot(1, mock_time_slot_create)
        
        assert "пересекается" in str(exc_info.value)