from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.api_exception_handlers import http_exception_handler, unhandled_exception_handler
from app.db.session import get_db
from app.features.upload_bottle import routers
from app.features.upload_bottle.routers import router as upload_bottle_router
from app.features.upload_bottle.schemas import BottleResponse


def _build_test_app() -> FastAPI:
    """
    Build a minimal FastAPI app wired with only the bottle router and the
    same global exception handlers as the real app. This avoids importing
    app.main, which constructs Settings() at import time and therefore
    requires environment configuration that test environments (like CI)
    don't provide.
    """
    bottle_test_app = FastAPI()
    bottle_test_app.add_exception_handler(HTTPException, http_exception_handler)
    bottle_test_app.add_exception_handler(Exception, unhandled_exception_handler)
    bottle_test_app.include_router(upload_bottle_router, prefix="/bottles")
    return bottle_test_app


_test_app = _build_test_app()


@pytest.fixture()
def client():
    """Provide a TestClient with the database dependency overridden by a mock session, isolating router tests from real database infrastructure."""
    _test_app.dependency_overrides[get_db] = lambda: MagicMock(spec=Session)
    yield TestClient(_test_app)
    _test_app.dependency_overrides.clear()


def _build_upload_payload() -> dict:
    """Build a minimal multipart file payload for posting to the upload endpoint."""
    return {"file": ("bottle.jpg", b"fake-image-bytes", "image/jpeg")}


# ======================================================================
# POST /bottles/
# ======================================================================


def test_create_bottle_record_returns_created_with_payload_on_success(monkeypatch, client):
    """
    Check that the route returns 201 with the service's response wrapped in
    the standard success envelope when the service layer succeeds.
    """
    expected_response = BottleResponse(id=uuid4(), brand_name="Tylenol")
    mock_service_instance = MagicMock()
    mock_service_instance.create_bottle.return_value = expected_response
    monkeypatch.setattr(routers, "BottleService", lambda _db: mock_service_instance)

    response = client.post("/bottles/", files=_build_upload_payload())

    assert response.status_code == status.HTTP_201_CREATED
    response_body = response.json()
    assert response_body["success"] is True
    assert response_body["payload"]["id"] == str(expected_response.id)
    assert response_body["payload"]["brand_name"] == "Tylenol"


def test_create_bottle_record_propagates_http_exception_from_service(monkeypatch, client):
    """
    Check that the route re-raises an HTTPException from the service layer
    with its original status code and detail message intact.
    """
    mock_service_instance = MagicMock()
    mock_service_instance.create_bottle.side_effect = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        detail="No readable text was found on the label. Try uploading a clearer, well-lit photo."
    )
    monkeypatch.setattr(routers, "BottleService", lambda _db: mock_service_instance)

    response = client.post("/bottles/", files=_build_upload_payload())

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    response_body = response.json()
    assert response_body["success"] is False
    assert response_body["detail"] == "No readable text was found on the label. Try uploading a clearer, well-lit photo."


def test_create_bottle_record_wraps_unexpected_exception_as_internal_server_error(monkeypatch, client):
    """
    Check that the route converts an unexpected exception escaping the service
    layer into a 500 response using the router's own wrapper message.
    """
    mock_service_instance = MagicMock()
    mock_service_instance.create_bottle.side_effect = RuntimeError("simulated unexpected failure")
    monkeypatch.setattr(routers, "BottleService", lambda _db: mock_service_instance)

    response = client.post("/bottles/", files=_build_upload_payload())

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    response_body = response.json()
    assert response_body["success"] is False
    assert response_body["detail"] == "An unexpected error occurred on the application server wrapper."
