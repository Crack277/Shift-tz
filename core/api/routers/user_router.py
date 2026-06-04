from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core.api.services.user_service import UserService
from core.database_helper import db_helper


router = APIRouter(prefix="/users")


@router.get("/")
async def get_users(session: AsyncSession = Depends(db_helper.session_dependency)):
    service = UserService(session)
    return await service.get_users()