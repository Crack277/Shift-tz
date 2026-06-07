from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.models.user import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_users(self) -> List[User]:
        stmt = select(User).order_by(User.id)
        result = await self.session.execute(stmt)
        users = result.scalars().all()
        return list(users)