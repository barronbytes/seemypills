from datetime import time, timedelta, timezone

from sqlalchemy import String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import PrimaryKeyMixin, TimestampMixin


class DeviceUsage(Base, PrimaryKeyMixin, TimestampMixin):
    """
    Defines table for storing usage limit data. 
    Total daily unique users limited by device fingerprint.
    Individual user usage limited by the hour.
    """
    __tablename__ = "device_usage"

    RATE_LIMIT_DURATION: timedelta = timedelta(hours=1)
    DAILY_RESET_TIME: time = time(0, 0, tzinfo=timezone.utc)
    HOURLY_SINGLE_USER_USAGE_LIMIT: int = 10
    DAILY_TOTAL_UNIQUE_DEVICES_LIMIT: int = 20

    device_fingerprint: Mapped[str] = mapped_column(String, unique=True)
    hourly_user_usage: Mapped[int] = mapped_column(default=0)

    @hybrid_property
    def attempts_remaining(self) -> int:
        remaining = self.HOURLY_SINGLE_USER_USAGE_LIMIT - self.hourly_user_usage       
        return max(0, remaining)