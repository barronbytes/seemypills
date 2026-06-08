from sqlalchemy.orm import Session

from app.features.device_usage.schemas import (
    DeviceUsageCreate,
    DeviceUsageResponse
)


class DeviceService:
    """Manages business logic, rate limits, and persistence for device metrics."""

    def __init__(self, db: Session) -> None:
        """ Initialize the service and inject the persistence layer database session."""
        self.db = db

    # ======================================================================
    # CREATE
    # ======================================================================

    def create_device(self, device_data: DeviceUsageCreate) -> DeviceUsageResponse:
        """Create a new unique device tracking instance."""
        pass

    # ======================================================================
    # READ
    # ======================================================================

    def get_daily_unique_device_count(self) -> int:
        """Query the database for count of all devices permitted to interact with app since DAILY_RESET_TIME"""
        pass

    def get_device_by_fingerprint(self, device_fingerprint: str) -> DeviceUsageResponse | None:
        """Query the database for a record matching a unique fingerprint string."""
        pass

    # ======================================================================
    # UPDATE
    # ======================================================================

    def increment_device_usage(self, device_fingerprint: str) -> DeviceUsageResponse:
        """Update device usage count for successfully performed actions."""
        pass

    def reset_hourly_usages(self) -> int:
        """Update ALL records to reset hourly counters for non-deleted acounts."""
        pass

    # ======================================================================
    # DELETE (softly)
    # ======================================================================

    def soft_delete_device(self, device_fingerprint: str) -> DeviceUsageResponse:
        """Delete a record softly with soft_delete mixin"""
        pass