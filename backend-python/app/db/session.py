from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session per request.

    Requires setup_database() to be called first during application startup.

    If setup_database() has not been called:
        - SessionLocal will be None
        - a RuntimeError will be raised

    Lifecycle:
        create session → yield to request → close session after request
    """
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call setup_database() first.")

    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


# Database sessions for router layer
SessionPublic = Annotated[Session, Depends(get_db)]