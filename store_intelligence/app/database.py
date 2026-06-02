from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Engine setup backed by explicit connection configuration pools
engine = create_engine(
    settings.DATABASE_URL, 
    pool_size=20, 
    max_overflow=10,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Contextual generator ensuring safe request-scoped lifecycle operations."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()