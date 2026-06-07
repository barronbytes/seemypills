from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import PrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from app.features.device_usage.models import Device


class Bottle(Base, PrimaryKeyMixin, TimestampMixin):
    """
    Defines table for storing extracted medication bottle information.
    Requires a valid relation to a originating tracking device.
    Brand_name is the only required data point right now.
    """
    __tablename__ = "pill_bottle"

    device_id: Mapped[UUID] = mapped_column(
        ForeignKey("device_usage.id", ondelete="CASCADE"), 
        nullable=False
    )

    brand_name: Mapped[str] = mapped_column(String, nullable=False)
    generic_name: Mapped[str | None] = mapped_column(String, default=None)
    dosage: Mapped[str | None] = mapped_column(String, default=None)
    dosage_frequency: Mapped[str | None] = mapped_column(String, default=None)
    prescribing_doctor: Mapped[str | None] = mapped_column(String, default=None)
    expiration_date: Mapped[str | None] = mapped_column(String, default=None)
    ocr_raw_text: Mapped[str | None] = mapped_column(Text, default=None)

    device: Mapped["Device"] = relationship(back_populates="bottles")