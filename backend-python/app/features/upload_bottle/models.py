from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import PrimaryKeyMixin, TimestampMixin, SoftDeleteMixin


class Bottle(Base, PrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """
    Defines table for storing extracted medication bottle information.
    Requires a valid relation to an originating tracking device.
    Both brand_name and ocr_raw_text are strictly required data points.
    """
    __tablename__ = "pill_bottle"


    brand_name: Mapped[str] = mapped_column(String)
    ocr_raw_text: Mapped[str] = mapped_column(Text)