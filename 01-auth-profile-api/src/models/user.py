"""
User model (maps to a PostgreSQL table).

Easy idea:
- This class is like a "template" of a row in the users table.
- Each instance of User = one row in the DB.

Why:
- Keeps DB structure defined in code (clean + maintainable).
- SQLAlchemy will generate SQL queries for us.
"""

import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class User(Base):
    """
    `__tablename__` is the actual table name in PostgreSQL.
    """
    __tablename__ = "users"

    # Primary Key:
    # - We use UUID so IDs are hard to guess (nice for security).
    # - default=uuid.uuid4 creates a new UUID automatically.
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Email:
    # - unique=True means DB will reject duplicates (best practice).
    # - index=True makes lookups faster (login checks email often).
    email: Mapped[str] = mapped_column(
        String(225),
        unique=True,
        index=True,
        nullable=False
    )

    # password hash:
    # - store hash only, never raw password.
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

     # Name:
    # - simple profile field.
    name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    # Timestamps:
    # - server_default=func.now() lets DB fill the time automatically.
    # - onupdate=func.now() updates timestamp when row changes.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

