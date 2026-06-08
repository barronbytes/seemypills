import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException

from app.core.api_exception_handlers import http_exception_handler, unhandled_exception_handler
from app.core.config import get_settings
from app.db.database import setup_database
from app.features.upload_bottle.routers import router as upload_bottle_router

logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Initialize the database engine and session factory before the app serves requests."""
    logger.info(
        f"Starting {settings.app_info.app_name} "
        f"(environment={settings.app_info.env}, debug={settings.app_info.debug})"
    )
    setup_database()
    yield
    logger.info(f"Shutting down {settings.app_info.app_name}")


app = FastAPI(
    title=settings.app_info.app_name,
    version=settings.app_info.app_version,
    debug=settings.app_info.debug,
    description="Processes photos of prescription bottle labels and returns medication dosage information for audio-visual playback.",
    lifespan=lifespan
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(upload_bottle_router, prefix="/bottles")
