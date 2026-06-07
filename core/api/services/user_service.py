from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.api.repositories.user_repository import UserRepository
from core.models.user import User

class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)
        self.session = session
    
    async def get_users(self) -> List[User]:
        return await self.repository.get_users()
    