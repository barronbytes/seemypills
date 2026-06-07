import io
from pathlib import Path
from unittest.mock import MagicMock
from uuid import uuid4

import numpy as np
import pytest
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.features.upload_bottle.schemas import BottleResponse
from app.features.upload_bottle.services import BottleService


ASSETS_DIR = Path(__file__).parent / "assets"


class _FakeUploadFile:
    """Minimal stand-in for FastAPI's UploadFile exposing only what _decode_bottle_image touches."""

    def __init__(self, content_type: str, raw_bytes: bytes) -> None:
        self.content_type = content_type
        self.file = io.BytesIO(raw_bytes)

    def close(self) -> None:
        self.file.close()


def _build_upload_file(filename: str, content_type: str) -> _FakeUploadFile:
    """Wrap a saved test asset's bytes in a fake upload file for service-layer testing."""
    raw_bytes = (ASSETS_DIR / filename).read_bytes()
    return _FakeUploadFile(content_type=content_type, raw_bytes=raw_bytes)


# ======================================================================
# _decode_bottle_image
# ======================================================================


def test_decode_bottle_image_with_real_photo_succeeds():
    """
    Check that _decode_bottle_image decodes a real bottle photo into an image matrix.
    """
    service = BottleService(db=MagicMock(spec=Session))
    upload_file = _build_upload_file("bottle_from_otc.jpg", content_type="image/jpeg")

    decoded_image = service._decode_bottle_image(upload_file)

    assert isinstance(decoded_image, np.ndarray)


def test_decode_bottle_image_with_wrong_file_format_fails():
    """
    Check that _decode_bottle_image raises HTTPException when the uploaded
    file is not an image format.
    """
    service = BottleService(db=MagicMock(spec=Session))
    upload_file = _build_upload_file("hello_world.txt", content_type="text/plain")

    with pytest.raises(HTTPException) as exc_info:
        service._decode_bottle_image(upload_file)

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST


# ======================================================================
# _run_ocr_pipeline
# ======================================================================


@pytest.mark.integration
def test_run_ocr_pipeline_with_real_photo_succeeds():
    """
    Check that _run_ocr_pipeline extracts a brand name and raw text from a
    decoded real bottle photo, with the raw text longer than the brand name.
    """
    service = BottleService(db=MagicMock(spec=Session))
    upload_file = _build_upload_file("bottle_from_otc.jpg", content_type="image/jpeg")
    decoded_image = service._decode_bottle_image(upload_file)

    parsed_brand_name, extracted_raw_text = service._run_ocr_pipeline(decoded_image)

    assert isinstance(parsed_brand_name, str) and parsed_brand_name
    assert isinstance(extracted_raw_text, str) and extracted_raw_text
    assert len(extracted_raw_text) > len(parsed_brand_name)


@pytest.mark.integration
def test_run_ocr_pipeline_with_blank_image_fails():
    """
    Check that _run_ocr_pipeline raises HTTPException when the OCR engine
    detects no readable text in a decoded blank image.
    """
    service = BottleService(db=MagicMock(spec=Session))
    upload_file = _build_upload_file("blank_photo.png", content_type="image/png")
    decoded_image = service._decode_bottle_image(upload_file)

    with pytest.raises(HTTPException) as exc_info:
        service._run_ocr_pipeline(decoded_image)

    assert exc_info.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "No readable text" in exc_info.value.detail


@pytest.mark.integration
def test_run_ocr_pipeline_with_malformed_image_matrix_fails():
    """
    Check that _run_ocr_pipeline raises HTTPException when given an array
    that is not a valid image matrix and the OCR engine fails internally.
    """
    service = BottleService(db=MagicMock(spec=Session))
    malformed_image = np.array([1, 2, 3])

    with pytest.raises(HTTPException) as exc_info:
        service._run_ocr_pipeline(malformed_image)

    assert exc_info.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "Unable to successfully extract textual details" in exc_info.value.detail


# ======================================================================
# create_bottle
# ======================================================================


def test_create_bottle_persists_record_and_returns_response_succeeds(monkeypatch):
    """
    Check that create_bottle persists the mapped Bottle record and returns
    a BottleResponse when the database transaction succeeds.
    """
    mock_db = MagicMock(spec=Session)
    mock_db.refresh.side_effect = lambda instance: setattr(instance, "id", uuid4())
    service = BottleService(db=mock_db)
    monkeypatch.setattr(service, "_extract_bottle_text", lambda _file: ("Tylenol", "TYLENOL EXTRA STRENGTH 500MG"))

    response = service.create_bottle(file=MagicMock())

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
    assert isinstance(response, BottleResponse)
    assert response.brand_name == "Tylenol"


def test_create_bottle_rolls_back_and_raises_on_database_error_fails(monkeypatch):
    """
    Check that create_bottle rolls back the transaction and raises HTTPException
    when the database commit fails with a structural SQLAlchemy error.
    """
    mock_db = MagicMock(spec=Session)
    mock_db.commit.side_effect = SQLAlchemyError("simulated database failure")
    service = BottleService(db=mock_db)
    monkeypatch.setattr(service, "_extract_bottle_text", lambda _file: ("Tylenol", "TYLENOL EXTRA STRENGTH 500MG"))

    with pytest.raises(HTTPException) as exc_info:
        service.create_bottle(file=MagicMock())

    mock_db.rollback.assert_called_once()
    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
