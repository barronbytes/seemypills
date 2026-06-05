import pytest

from sqlalchemy import text, create_engine

import app.db.database as database
from app.core.config import get_settings


@pytest.mark.integration
def test_local_db_connection_passes():
    """
    Check SQLAlchemy connection to local PostgreSQL database.
    ENV=development by default.
    """

    database.setup_database()

    assert database.engine is not None

    with database.engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        value = result.scalar()

    assert value == 1


@pytest.mark.integration
def test_aws_rds_connection_passes(monkeypatch):
    """
    Check SQLAlchemy connection to AWS RDS database.
    ENV=production temporarily set by monkeypatch.setenv()
    """
    monkeypatch.setenv("ENV", "production")
    prod_settings = get_settings()
    prod_engine = create_engine(prod_settings.db_info.db_url)

    # 4. Execute the live network query against your cloud AWS RDS instance
    with prod_engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        value = result.scalar()

    # 5. Assert that the database successfully processed and returned the token
    assert value == 1