"""
Profile routes.

Why:
- Separate profile operations from auth operations.
- All these routes require authentication.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.core.deps import get_current_user
from src.models.user import User
from src.schemas.user import UserPublic, UpdateProfileRequest, user_to_public
from src.services.profile_service import update_profile


router = APIRouter(prefix="/me", tags=["profile"])


@router.get("", response_model=UserPublic)
def get_profile(user: User = Depends(get_current_user)):
    """
    Get current user's profile.
    
    Why:
    - Frontend needs to display user info.
    - get_current_user already loaded and verified the user.
    
    Security:
    - Requires valid JWT token in Authorization header.
    - Returns only public fields (no password_hash).
    """
    return user_to_public(user)


@router.patch("", response_model=UserPublic)
def update_profile_endpoint(
    payload: UpdateProfileRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update current user's profile.
    
    What you can update:
    - name
    - bio
    
    What you CANNOT update here:
    - email (needs verification flow)
    - password (needs current password verification)
    - id (never changeable)
    - timestamps (auto-managed)
    
    Why PATCH not PUT:
    - PATCH = partial update (send only fields you want to change)
    - PUT = full replacement (would require sending all fields)
    """
    updated_user = update_profile(db, user=user, updates=payload)
    return user_to_public(updated_user)
