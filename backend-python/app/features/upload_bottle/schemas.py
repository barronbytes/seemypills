from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class BottleBase(BaseModel):
    brand_name: str


class BottleCreate(BottleBase):
    brand_name: str | None = None
    ocr_raw_text: str | None = None         # source of truth


class BottleResponse(BottleBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    brand_name: str | None


class BottleUpdate(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    brand_name: str | None = Field(default=None)


class BottleDelete(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    deleted_at: datetime | None = Field(default=None)