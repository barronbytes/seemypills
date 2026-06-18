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
        self.size = len(raw_bytes)
        self.file = io.BytesIO(raw_bytes)

    def close(self) -> None:
        self.file.close()


def _build_upload_file(filename: str, content_type: str) -> _FakeUploadFile:
    """Wrap a saved test asset's bytes in a fake upload file for service-layer testing."""
    raw_bytes = (ASSETS_DIR / filename).read_bytes()
    return _FakeUploadFile(content_type=content_type, raw_bytes=raw_bytes)


# ======================================================================
# _bounded_box_heuristic
# ======================================================================


def test_bounded_box_heuristic_prioritizes_tall_box_over_wide_box_of_equal_area():
    """
    Check that _bounded_box_heuristic scores a tall, narrow box higher than a
    short, wide box of the same total area, matching the documented 60%
    height weighting that prioritizes brand name text over manufacturer labels.
    """
    tall_narrow_box = [[0, 0], [2, 0], [2, 12], [0, 12]]
    short_wide_box = [[0, 0], [12, 0], [12, 2], [0, 2]]

    tall_score = BottleService._bounded_box_heuristic(tall_narrow_box)
    wide_score = BottleService._bounded_box_heuristic(short_wide_box)

    assert tall_score > wide_score


def test_bounded_box_heuristic_with_zero_height_returns_zero():
    """
    Check that _bounded_box_heuristic returns 0.0 for a degenerate OCR
    fragment with no perpendicular height between its top and bottom edges.
    """
    zero_height_box = [[0, 0], [10, 0], [10, 0], [0, 0]]

    score = BottleService._bounded_box_heuristic(zero_height_box)

    assert score == 0.0


def test_bounded_box_heuristic_with_zero_width_returns_zero():
    """
    Check that _bounded_box_heuristic returns 0.0 for a degenerate OCR
    fragment with no width between its left and right edges, even though
    its height is nonzero.
    """
    zero_width_box = [[0, 0], [0, 0], [0, 5], [0, 5]]

    score = BottleService._bounded_box_heuristic(zero_width_box)

    assert score == 0.0


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


def test_decode_bottle_image_with_oversized_payload_fails():
    """
    Check that _decode_bottle_image raises HTTPException when the uploaded
    file's payload size meets or exceeds the 7MB limit.
    """
    service = BottleService(db=MagicMock(spec=Session))
    oversized_bytes = b"\x00" * (7 * 1024 * 1024)
    upload_file = _FakeUploadFile(content_type="image/jpeg", raw_bytes=oversized_bytes)

    with pytest.raises(HTTPException) as exc_info:
        service._decode_bottle_image(upload_file)

    assert exc_info.value.status_code == status.HTTP_413_CONTENT_TOO_LARGE


def test_decode_bottle_image_with_invalid_content_type_header_fails():
    """
    Check that _decode_bottle_image raises HTTPException when the uploaded
    file's Content-Type header is not an image format.
    """
    service = BottleService(db=MagicMock(spec=Session))
    upload_file = _build_upload_file("hello_world.txt", content_type="text/plain")

    with pytest.raises(HTTPException) as exc_info:
        service._decode_bottle_image(upload_file)

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST


def test_decode_bottle_image_with_mismatched_magic_bytes_fails():
    """
    Check that _decode_bottle_image raises HTTPException when the uploaded
    file's Content-Type header claims an image format but its magic bytes
    do not match a supported JPEG or PNG signature.
    """
    service = BottleService(db=MagicMock(spec=Session))
    upload_file = _build_upload_file("hello_world.txt", content_type="image/png")

    with pytest.raises(HTTPException) as exc_info:
        service._decode_bottle_image(upload_file)

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid image structure" in exc_info.value.detail


# ======================================================================
# _run_ocr_pipeline
# ======================================================================


@pytest.fixture(scope="module")
def _shared_ocr_reader():
    """
    Load the EasyOCR model once for this module and patch easyocr.Reader to
    return that single instance, so the three integration tests below share
    one set of ML weights in memory instead of each loading its own.
    """
    import easyocr

    monkeypatch = pytest.MonkeyPatch()
    shared_reader = easyocr.Reader(['en'], gpu=False)
    monkeypatch.setattr(easyocr, "Reader", lambda *args, **kwargs: shared_reader)

    yield

    monkeypatch.undo()


@pytest.mark.integration
def test_run_ocr_pipeline_with_real_photo_succeeds(_shared_ocr_reader):
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
def test_run_ocr_pipeline_with_blank_image_fails(_shared_ocr_reader):
    """
    Check that _run_ocr_pipeline raises HTTPException when the OCR engine
    detects no readable text in a decoded blank image.
    """
    service = BottleService(db=MagicMock(spec=Session))
    upload_file = _build_upload_file("blank_photo.png", content_type="image/png")
    decoded_image = service._decode_bottle_image(upload_file)

    with pytest.raises(HTTPException) as exc_info:
        service._run_ocr_pipeline(decoded_image)

    assert exc_info.value.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert "No readable text" in exc_info.value.detail


@pytest.mark.integration
def test_run_ocr_pipeline_with_malformed_image_matrix_fails(_shared_ocr_reader):
    """
    Check that _run_ocr_pipeline raises HTTPException when given an array
    that is not a valid image matrix and the OCR engine fails internally.
    """
    service = BottleService(db=MagicMock(spec=Session))
    malformed_image = np.array([1, 2, 3])

    with pytest.raises(HTTPException) as exc_info:
        service._run_ocr_pipeline(malformed_image)

    assert exc_info.value.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
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
