from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

db_url = settings.db_info.db_url

engine = create_engine(
    url=db_url,
    pool_size=5,
    max_overflow=10,
    pool_recycle=1800, # proactive hygeine: retires live connect, creates new connection
    pool_pre_ping=True # reactive hygiene: retires dead connection, makes new connection
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()