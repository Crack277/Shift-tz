from fastapi import FastAPI
import uvicorn

from core.api import router as api_router

from core.config import settings


app = FastAPI()
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)