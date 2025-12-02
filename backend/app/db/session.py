# backend/app/db/session.py
"""
Database session configuration.
This is an example of how to make your session.py test-friendly.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create engine based on DATABASE_URL from settings
# In test mode, this will use SQLite :memory:
engine = create_engine(
    settings.DATABASE_URL,
    # SQLite-specific args (ignored for PostgreSQL)
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    # Pool settings for PostgreSQL
    pool_pre_ping=True if "postgresql" in settings.DATABASE_URL else False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()