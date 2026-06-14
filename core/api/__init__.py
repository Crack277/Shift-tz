from fastapi import APIRouter

from core.config import settings

from .routers.user_router import router as user_router
from .routers.auth_router import router as auth_router
from .routers.room_router import router as room_router
from .routers.reservation_router import router as reservation_router

router = APIRouter(prefix=settings.api.prefix)
router.include_router(user_router)
router.include_router(auth_router)
router.include_router(room_router)
router.include_router(reservation_router)
