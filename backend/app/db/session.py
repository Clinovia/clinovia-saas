from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.config import settings

# Detect if using SQLite or Postgres
if "sqlite" in settings.sqlalchemy_url:
    engine = create_engine(
        settings.sqlalchemy_url,
        connect_args={"check_same_thread": False},
    )
else:
    engine = create_engine(
        settings.sqlalchemy_url,
        connect_args={"sslmode": "require"},  # required for Supabase
        pool_pre_ping=True,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
