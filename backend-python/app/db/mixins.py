import uuid
from datetime import datetime, timezone

from sqlalchemy import UUID as DB_UUID, func
from sqlalchemy.orm import Mapped, mapped_column


def _utc_now():
    """Helper function to return a SQL expression for the current UTC timestamp."""
    return func.timezone(
        "UTC",      # timezone
        func.now()  # timestamp expression
    )


class PrimaryKeyMixin:
    """Add id column to models."""

    id: Mapped[uuid.UUID] = mapped_column(
        DB_UUID(as_uuid=True), # Ensures database uses the native UUID type
        primary_key=True,
        default=uuid.uuid4
    )


class TimestampMixin:
    """Add columns for created_at and updated_at to models."""

    created_at: Mapped[datetime] = mapped_column(
        server_default=_utc_now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=_utc_now(),
        server_onupdate=_utc_now()
    )


class SoftDeleteMixin:
    """Add soft delete support to models."""

    deleted_at: Mapped[datetime | None] = mapped_column(default=None)

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def soft_delete(self) -> None:
        self.deleted_at = datetime.now(timezone.utc)

    def restore(self) -> None:
        self.deleted_at = None
