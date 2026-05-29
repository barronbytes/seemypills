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
        pool_recycle=1800, # proactive hygeine: retires live connect, creates new connection
        pool_pre_ping=True # reactive hygiene: retires dead connection, makes new connection
    )
    
    SessionLocal = sessionmaker(
        autocommit=False, 
        autoflush=False, 
        bind=engine
    )