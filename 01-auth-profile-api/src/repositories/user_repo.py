"""
User repository: ONLY database operations.

Why:
- Keeps SQLAlchemy queries in one place.
- Makes service layer simple and readable.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select

from src.models.user import User


def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Find a user by email.

    Why:
    - During register, we need to check if email already exists.
    - During login, we’ll also use this.
    """
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalar_one_or_none()


def create_user(db: Session, *, email: str, password_hash: str, name: str) -> User:
    """
    Insert a new user.

    Why:
    - DB insert should be done in one place.
    - commit() saves changes.
    - refresh() loads generated fields (id, timestamps) into the object.
    """
    user = User(email=email, password_hash=password_hash, name=name)

    db.add(user)
    db.commit()
    db.refresh(user)  # now user.id, created_at etc are available

    return user
