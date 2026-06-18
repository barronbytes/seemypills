from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import get_settings

engine: Engine | None = None
SessionLocal: sessionmaker[Session] | None = None


def setup_database() -> None:
    """
    Initializes database engine and session factory.

    This must be called once during application startup BEFORE any call to get_db().

    Without this, SessionLocal will be None and database access will fail.
    """
    global engine, SessionLocal

    settings = get_settings()

    engine = create_engine(
        url=settings.db_info.db_url,
        pool_size=5,
        max_overflow=10,
        pool_timeout=15,    # structural hygiene: fails fast if a connection isn't available within 15 seconds to prevent server gridlock
        pool_recycle=1800,  # proactive hygiene: clears connections every 30 minutes to avoid network timeout disconnects
        pool_pre_ping=True  # reactive hygiene: double-checks every connection right before using it to guarantee API routes never crash from a dead socket
    )
    
    SessionLocal = sessionmaker(
        autocommit=False, 
        autoflush=False, 
        bind=engine
    )