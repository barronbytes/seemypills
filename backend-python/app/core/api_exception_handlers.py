import logging

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse

from app.core.api_response_schemas import ErrorResponse

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Wraps raised HTTPExceptions in the global error response envelope."""
    logger.warning(f"Global handler intercepted HTTP exception -> Status {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(detail=exc.detail).model_dump()
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Wraps unhandled exceptions in the global error response envelope."""
    logger.critical(f"Global handler intercepted unhandled exception -> {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(detail="An unexpected error occurred on the application server.").model_dump()
    )
