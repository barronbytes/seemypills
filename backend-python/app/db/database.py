from typing import Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import get_settings


engine: Engine | None = None
SessionLocal: sessionmaker[Session] | None = None


def setup_database() -> None:
    """
    Initializes database engine and session factory.

    Must be called once at application startup before any call to get_db().
    """
    global engine, SessionLocal

    settings = get_settings()

    engine = create_engine(
        url=settings.db_info.db_url,
        pool_size=5,
        max_overflow=10,
        pool_recycle=1800, # proactive hygeine: retires live connect, creates new connection
        pool_pre_ping=True # reactive hygiene: retires dead connection, makes new connection
    )
    
    SessionLocal = sessionmaker(
        autocommit=False, 
        autoflush=False, 
        bind=engine
    )


def get_db() -> Generator[Session, None, None]:
    """
    Creates new sessions per request and performs cleanup.

    Requires setup_database() to have been called first.

    Generator is the proper return type hint because of workflow:
        run → pause (yield) → resume → cleanup
    """
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call setup_database() first.")

    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()