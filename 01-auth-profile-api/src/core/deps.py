"""
FastAPI dependencies for authentication.

Why:
- Dependencies are reusable pieces of logic.
- Protected routes can just add `user: User = Depends(get_current_user)`.
- Keeps route code clean and DRY.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.core.tokens import decode_access_token
from src.db.session import get_db
from src.repositories.user_repo import get_user_by_id
from src.models.user import User


# HTTPBearer automatically extracts "Authorization: Bearer <token>" header
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    Extract and verify JWT token, then load user from DB.
    
    Flow:
    1. HTTPBearer extracts token from Authorization header
    2. decode_access_token verifies JWT signature + expiry
    3. Load user from DB using user_id from token
    4. Return user object
    
    Returns:
    - User object if everything is valid
    
    Raises:
    - 401 if token is missing, invalid, expired, or user not found
    
    Usage in routes:
    ```python
    @router.get("/me")
    def get_profile(user: User = Depends(get_current_user)):
        # user is already loaded and verified
        return {"email": user.email}
    ```
    """
    token = credentials.credentials
    
    # Decode and verify token
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    
    # Load user from DB
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    return user
