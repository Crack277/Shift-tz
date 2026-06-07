from fastapi import FastAPI
import uvicorn

from contextlib import asynccontextmanager

from core.api import router as api_router
from core.config import settings
from core.database_helper import db_helper
from core.models import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await db_helper.engine.dispose()



app = FastAPI(lifespan=lifespan)
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)