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
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class GUID(TypeDecorator):
    """
    Platform-independent GUID type.
    
    Why:
    - PostgreSQL has native UUID support.
    - SQLite doesn't, so we store as CHAR(36).
    - This makes tests work with SQLite and production with PostgreSQL.
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return value
        else:
            if isinstance(value, uuid.UUID):
                return str(value)
            return value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return value
        return uuid.UUID(value)


class User(Base):
    """
    `__tablename__` is the actual table name in PostgreSQL.
    """
    __tablename__ = "users"

    # Primary Key:
    # - We use UUID so IDs are hard to guess (nice for security).
    # - default=uuid.uuid4 creates a new UUID automatically.
    # - GUID type works with both PostgreSQL and SQLite.
    id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
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

    # Bio (optional):
    # - user's short description about themselves.
    bio: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
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

