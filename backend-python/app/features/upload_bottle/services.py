import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import UploadFile, HTTPException, status

from app.features.upload_bottle.schemas import (
    BottleCreate,
    BottleResponse
)
from app.features.upload_bottle.models import Bottle

logger = logging.getLogger(__name__)

class BottleService:
    """Manages business logic, OCR extraction tracking, and persistence for uploaded medication bottles."""

    def __init__(self, db: Session) -> None:
        """Initialize the service and inject the persistence layer database session."""
        self.db = db

    # =========================================================================
    # CREATE
    # =========================================================================

    def create_bottle(self, bottle_data: BottleCreate, file: UploadFile) -> BottleResponse:
        """Create a new medication bottle record with extracted photo text."""
        
        # I. PERMISSIONS (RBAC/ABAC)
        logger.info("Phase I (Permissions): Checking request authorization constraints.")
        logger.info("Phase I (Permissions): Success. Authorization check bypassed for MVP.")

        # II. GUARDRAILS (VALIDATE)
        # Exit if wrong file type
        if not file.content_type.startswith("image/"):
            logger.error(f"Validation failed. Rejected invalid file format: {file.content_type}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file must be a valid image format (PNG/JPEG)."
            )

        try:
            # Lazy import heavy ML libraries to reduce app load latency
            import cv2
            import easyocr
            import numpy as np

            logger.info(f"Processing image upload for device.")
            image_bytes = file.file.read()
            
            # Convert raw file memory buffer straight into an OpenCV numeric matrix
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                raise ValueError("OpenCV failed to decode binary matrix stream.")

            # TODO: Add custom OpenCV processing adjustments (grayscale, thresholding, etc.)

            # 3. Fire up the EasyOCR reading engine targeting English medical labels
            reader = easyocr.Reader(['en'], gpu=False)  # Set to True if infrastructure utilizes CUDA
            ocr_results = reader.readtext(img, detail=0)
            
            # Combine array list segments cleanly into a single target string block
            extracted_raw_text = " ".join(ocr_results).strip()
            logger.info("OCR raw text block reading successfully concluded.")

            # TODO: Insert your string parsing heuristics here to evaluate raw string into a brand name.
            # For MVP demo fallback purposes, we default to the schema's raw string or fallback string.
            parsed_brand_name = bottle_data.brand_name if bottle_data.brand_name else "Extracted Generic Label"

        except Exception as ocr_err:
            logger.exception(f"Fatal processing failure inside internal ML OCR engine sequence: {str(ocr_err)}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Unable to successfully extract textual details from the provided image file."
            )

        # III. MAPPING (PYDANTIC ➔ SQLALCHEMY)
        logger.info("Phase III (Mapping): Converting Pydantic payload schema to SQLAlchemy database model.")
        db_bottle = Bottle(
            brand_name=parsed_brand_name,
            generic_name=bottle_data.generic_name,
            dosage=bottle_data.dosage,
            dosage_frequency=bottle_data.dosage_frequency,
            prescribing_doctor=bottle_data.prescribing_doctor,
            expiration_date=bottle_data.expiration_date,
            ocr_raw_text=extracted_raw_text
        )
        logger.info("Phase III (Mapping): Success. Conversion complete.")

        # IV. EXECUTION
        try:
            logger.info("Phase IV (Execution): Starting database persistence transaction.")
            self.db.add(db_bottle)
            self.db.commit()
            self.db.refresh(db_bottle)
            logger.info(f"Phase IV (Execution): Success. Bottle record created with ID: {db_bottle.id}")
            return BottleResponse.model_validate(db_bottle)
        # V. EXCEPTION HANDLING
        except SQLAlchemyError as db_err:
            logger.error("Phase V (Exception Handling): Intercepted structural transaction failure.")
            self.db.rollback()
            logger.critical(f"Phase V (Exception Handling): Failure detail -> {str(db_err)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="A structural database error occurred while trying to save transaction items safely."
            )