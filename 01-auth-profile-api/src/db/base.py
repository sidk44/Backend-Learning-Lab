"""
Base class for SQLAlchemy models.

Why:
- All models inherit from Base.
- Later, we can create tables from Base.metadata (simple start).
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass