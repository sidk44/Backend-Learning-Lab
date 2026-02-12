"""
Auth service: business logic for authentication.

Why:
- Service layer is where "rules" live.
- Route/controller stays thin and readable.
"""

from sqlalchemy.orm import Session

from src.core.security import hash_password, verify_password
from src.core.tokens import create_access_token
from src.repositories.user_repo import get_user_by_email, create_user


class EmailAlreadyExists(Exception):
    """
    Custom error so route can return 409 Conflict neatly.
    """
    pass


class InvalidCredentials(Exception):
    """
    Custom error for wrong email or password.
    
    Why:
    - Route can return 401 Unauthorized with a clean message.
    """
    pass


def register_user(db: Session, *, email: str, password: str, name: str):
    """
    Register a new user.

    Flow:
    1) Check if email exists
    2) Hash password
    3) Create user in DB
    4) Create access token
    5) Return (token, user)
    """
    existing = get_user_by_email(db, email)
    if existing:
        raise EmailAlreadyExists()

    password_hash = hash_password(password)
    user = create_user(db, email=email, password_hash=password_hash, name=name)

    token = create_access_token(str(user.id))

    return token, user


def login_user(db: Session, *, email: str, password: str):
    """
    Login an existing user.
    
    Flow:
    1) Find user by email
    2) Verify password against stored hash
    3) Create access token
    4) Return (token, user)
    
    Security:
    - We don't tell which is wrong (email vs password) to avoid user enumeration.
    - Just say "invalid credentials".
    """
    user = get_user_by_email(db, email)
    if not user:
        raise InvalidCredentials()
    
    if not verify_password(password, user.password_hash):
        raise InvalidCredentials()
    
    token = create_access_token(str(user.id))
    
    return token, user
