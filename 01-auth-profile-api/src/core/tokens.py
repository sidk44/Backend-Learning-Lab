"""
JWT token creation + verification.

Easy idea:
- Token is like a temporary ID card.
- Client sends it in Authorization header for protected routes.
"""

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

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


def decode_access_token(token: str) -> str | None:
    """
    Decode and verify a JWT token.
    
    Returns:
    - user_id (from 'sub' claim) if valid
    - None if invalid/expired
    
    Why:
    - Protected routes need to know which user is making the request.
    - JWT handles verification (signature + expiry) automatically.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id: str | None = payload.get("sub")
        return user_id
    except JWTError:
        # Token is invalid, expired, or malformed
        return None
