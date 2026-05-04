import uuid
from datetime import datetime

from sqlalchemy import UUID as DB_UUID, func
from sqlalchemy.orm import Mapped, mapped_column


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
        default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now()
    )
