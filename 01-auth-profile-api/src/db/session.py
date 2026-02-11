"""
Database session + engine setup.

Why:
- Engine is the "connection factory" to the DB.
- Session is what we use to run queries safely.
- We provide `get_db()` as a dependency so each request gets its own session.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.core.config import settings


# create_engine() sets up the DB connection pool
# pool_pre_ping helps avoid stale connections in long-running servers.

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

# sessionmaker creates Session objects.
# autocommit=False + autoflush = False is a common safe default.
SessionLocal = sessionmaker(bind= engine ,autoflush=False,autocommit=False
)

def get_db():

    """
    FastAPI dependency.

    Why:
    - Gives each request a DB session.
    - Ensures session is closed even if request fails.
    """

    db: Session = SessionLocal()

    try:
        yield db
    finally:
        db.close()

