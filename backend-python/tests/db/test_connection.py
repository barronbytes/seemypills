from sqlalchemy import text

import app.db.database as database

def test_local_db_connection_passes():
    """
    Check if SQLAlchemy connection to LOCAL PostgreSQL database works.
    Use .env.development file to construct database url from database.py
    """

    database.setup_database()

    assert database.engine is not None

    with database.engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        value = result.scalar()

    assert value == 1