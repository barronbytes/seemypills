from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import PrimaryKeyMixin, TimestampMixin


class Bottle(Base, PrimaryKeyMixin, TimestampMixin):
    """
    Defines table for storing extracted medication bottle information.
    Requires a valid relation to a originating tracking device.
    Brand_name is the only required data point right now.
    """
    __tablename__ = "pill_bottle"


    brand_name: Mapped[str] = mapped_column(String, nullable=False)
    ocr_raw_text: Mapped[str | None] = mapped_column(Text, default=None)