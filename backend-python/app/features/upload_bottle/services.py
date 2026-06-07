from sqlalchemy.orm import Session
from fastapi import UploadFile

from app.features.upload_bottle.schemas import (
    BottleCreate,
    BottleResponse
)


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
        pass