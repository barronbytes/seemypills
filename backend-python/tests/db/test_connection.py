import pytest

from sqlalchemy import create_engine, text

from app.db.database import get_settings

def test_local_db_connection_passes():
    """
    Check if SQLAlchemy connection to LOCAL PostgreSQL database works.
    Use .env.development file to construct database url from database.py
    """

    engine = create_engine(get_settings().db_info.db_url)

    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        value = result.scalar()

    assert value == 1