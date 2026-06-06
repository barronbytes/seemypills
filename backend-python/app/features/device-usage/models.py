from datetime import timedelta

from sqlalchemy import String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import PrimaryKeyMixin, TimestampMixin


class DeviceUsage(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "device_usage"

    RATE_LIMIT_COUNT: int = 10
    RATE_LIMIT_DURATION: timedelta = timedelta(hours=1)

    device_fingerprint: Mapped[str] = mapped_column(String, unique=True)
    rate_limit_usage: Mapped[int] = mapped_column(default=0)

    @hybrid_property
    def attempts_remaining(self) -> int:
        remaining = self.RATE_LIMIT_COUNT - self.rate_limit_usage        
        return max(0, remaining)