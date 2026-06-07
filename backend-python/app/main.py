from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.core.config import get_settings
from app.db.database import setup_database
from app.features.upload_bottle.routers import router as upload_bottle_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Initialize the database engine and session factory before the app serves requests."""
    setup_database()
    yield


app = FastAPI(
    title=settings.app_info.app_name,
    version=settings.app_info.app_version,
    debug=settings.app_info.debug,
    lifespan=lifespan
)

app.include_router(upload_bottle_router, prefix="/bottles")
