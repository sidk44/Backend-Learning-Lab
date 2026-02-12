"""
JWT token creation + verification.

Easy idea:
- Token is like a temporary ID card.
- Client sends it in Authorization header for protected routes.
"""

from datetime import datetime, timedelta, timezone
from jose import jwt

from src.core.config import settings


def create_access_token(user_id: str) -> str:
    """
    Create a signed JWT token.

    What we store inside:
    - sub (subject): user_id
    - exp: expiry time

    Why:
    - Server can verify token without storing sessions.
    - Expiry reduces damage if token is stolen.
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": user_id,
        "exp": expire,
    }

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
