# backend/app/db/init_db.py
import os

from app.db.session import Base, engine


def init_db():
    """
    Initialize the database schema.
    """
    print(f"Initializing DB for {os.getenv('ENVIRONMENT', 'development')}...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized!")


if __name__ == "__main__":
    init_db()
