from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from core.api.repositories.user_repository import UserRepository
from core.api.schemas.user_schemas import PrintToken, UserCreate
from core.api.utils import safety
from core.models import User


class UserService:
    """Сервис для управления пользователями"""

    def __init__(self, session: AsyncSession):
        self.user_repository = UserRepository(session)
        self.session = session

    async def get_users(self) -> List[User]:
        """Получить список всех пользователей"""
        return await self.user_repository.get_users()

    async def get_user_by_id(self, user_id: int) -> User:
        """Получить пользователя по ID"""
        return await self.user_repository.get_user_by_id(user_id=user_id)

    async def create_user(self, user_in: UserCreate) -> PrintToken:
        """
        Создать нового пользователя и вернуть JWT токен.
        """
        user = await self.user_repository.create_user(user_in=user_in)
        return safety.create_access_token(user=user)
