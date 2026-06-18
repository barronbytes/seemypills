import logging

from fastapi import APIRouter, UploadFile, File, HTTPException, status

from app.core.api_response_schemas import StandardResponse
from app.db.session import SessionPublic
from app.features.upload_bottle.schemas import BottleResponse
from app.features.upload_bottle.services import BottleService

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Medication Bottles"])

# ======================================================================
# # POST
# ======================================================================


@router.post(
    "/",
    response_model=StandardResponse[BottleResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Upload medication bottle image.",
    description="Processes an image of a medication bottle using OCR and saves the parsed brand name to the database."
)
async def create_bottle_record(
    db: SessionPublic,
    file: UploadFile = File(...)
) -> StandardResponse[BottleResponse]:
    """Endpoint route to receive form data photo uploads.
    No authentication required.
    """
    
    # I. INITIALIZE SERVICE
    logger.info("Phase I (Initialize Service): Injecting public database session dependency into service context.")
    bottle_service = BottleService(db)
    logger.info("Phase I (Initialize Service): Success. Service layer instantiated cleanly.")

    # II. EXECUTE SERVICE
    try:
        logger.info("Phase II (Execute Service): Handing off file asset tracking payload to internal service routines.")
        response_data = bottle_service.create_bottle(file=file)
        logger.info("Phase II (Execute Service): Success. Service layer transaction completed and returned data package.")
        return StandardResponse(payload=response_data)

    # III. EXCEPTION HANDLING
    except HTTPException as http_err:
        # CHECK #1: Catch and re-raise expected HTTP validations originating from service layer boundaries untouched
        logger.warning(f"Phase III (Exception Handling): Service level boundary gracefully rejected request -> Status {http_err.status_code}")
        raise http_err
        
    except Exception as unexpected_err:
        # CHECK #2: Catch-all guard for unhandled errors escaping the service scope execution matrices
        logger.error("Phase III (Exception Handling): Intercepted critical unhandled runtime error at the HTTP wrapper layer.")
        logger.critical(f"Phase III (Exception Handling): Failure detail -> {str(unexpected_err)}")
        logger.error(f"Router intercepted unhandled server execution failure: {str(unexpected_err)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred on the application server wrapper."
        )