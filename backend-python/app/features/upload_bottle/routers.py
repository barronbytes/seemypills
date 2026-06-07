import logging

from fastapi import APIRouter, UploadFile, File, HTTPException, status

from app.db.session import SessionPublic
from app.features.upload_bottle.schemas import BottleResponse
from app.features.upload_bottle.services import BottleService

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Medication Bottles"])


@router.post(
    "/",
    response_model=BottleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload medication bottle image",
    description="Processes an image of a medication bottle using OCR and saves the parsed brand name to the database."
)
async def create_bottle_record(
    db: SessionPublic,
    file: UploadFile = File(...)
) -> BottleResponse:
    """Endpoint route to receive form data photo uploads."""
    
    # 1. Initialize service
    bottle_service = BottleService(db)

    # 2. Execute service
    try:
        response_data = bottle_service.create_bottle(file=file)
        return response_data

    # 3. Exception Handling
    except HTTPException as http_err:
        # Re-raise known exceptions coming from the service layer boundaries untouched
        raise http_err
        
    except Exception as unexpected_err:
        # Catch-all guard for unhandled errors escaping the service scope execution matrices
        logger.error(f"Router intercepted unhandled server execution failure: {str(unexpected_err)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred on the application server wrapper."
        )