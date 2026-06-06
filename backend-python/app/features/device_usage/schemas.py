from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class DeviceUsageBase(BaseModel):
    device_fingerprint: str


class DeviceUsageCreate(DeviceUsageBase):
    pass


class DeviceUsageResponse(DeviceUsageBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    hourly_user_usage: int
    attempts_remaining: int     # pseudo-column that is calculated
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None


class DeviceUsageUpdate(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    hourly_user_usage: int | None = Field(default=None)


class DeviceUsageDelete(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    deleted_at: datetime | None = Field(default=None)