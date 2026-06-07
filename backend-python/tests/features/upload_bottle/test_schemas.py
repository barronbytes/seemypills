from datetime import datetime, timezone
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.features.upload_bottle.schemas import (
    BottleCreate,
    BottleResponse,
    BottleUpdate,
    BottleDelete,
)


# ======================================================================
# BottleCreate
# ======================================================================


def test_bottle_create_with_valid_data_succeeds():
    """
    Check that BottleCreate accepts a valid brand name and OCR text payload.
    """
    bottle_create = BottleCreate(brand_name="Tylenol", ocr_raw_text="TYLENOL EXTRA STRENGTH 500MG")

    assert bottle_create.brand_name == "Tylenol"
    assert bottle_create.ocr_raw_text == "TYLENOL EXTRA STRENGTH 500MG"


def test_bottle_create_missing_required_brand_name_fails():
    """
    Check that BottleCreate raises ValidationError when the required
    brand_name field is omitted.
    """
    with pytest.raises(ValidationError):
        BottleCreate(ocr_raw_text="TYLENOL EXTRA STRENGTH 500MG")


# ======================================================================
# BottleResponse
# ======================================================================


def test_bottle_response_with_valid_data_succeeds():
    """
    Check that BottleResponse accepts a valid id and brand name payload.
    """
    bottle_id = uuid4()
    bottle_response = BottleResponse(id=bottle_id, brand_name="Tylenol")

    assert bottle_response.id == bottle_id
    assert bottle_response.brand_name == "Tylenol"


def test_bottle_response_with_invalid_id_format_fails():
    """
    Check that BottleResponse raises ValidationError when id is not a valid UUID.
    """
    with pytest.raises(ValidationError):
        BottleResponse(id="not-a-valid-uuid", brand_name="Tylenol")


# ======================================================================
# BottleUpdate
# ======================================================================


def test_bottle_update_with_valid_data_succeeds():
    """
    Check that BottleUpdate accepts a valid brand name payload.
    """
    bottle_update = BottleUpdate(brand_name="Aspirin")

    assert bottle_update.brand_name == "Aspirin"


def test_bottle_update_with_invalid_brand_name_type_fails():
    """
    Check that BottleUpdate raises ValidationError when brand_name is not a valid string.
    """
    with pytest.raises(ValidationError):
        BottleUpdate(brand_name=123)


# ======================================================================
# BottleDelete
# ======================================================================


def test_bottle_delete_with_valid_data_succeeds():
    """
    Check that BottleDelete accepts a valid deleted_at timestamp payload.
    """
    deleted_timestamp = datetime.now(timezone.utc)
    bottle_delete = BottleDelete(deleted_at=deleted_timestamp)

    assert bottle_delete.deleted_at == deleted_timestamp


def test_bottle_delete_with_invalid_timestamp_format_fails():
    """
    Check that BottleDelete raises ValidationError when deleted_at is not a valid datetime.
    """
    with pytest.raises(ValidationError):
        BottleDelete(deleted_at="not-a-valid-timestamp")
