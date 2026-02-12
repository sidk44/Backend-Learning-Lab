"""
Profile service: business logic for profile operations.

Why:
- Keeps route handlers thin.
- Easy to test and maintain.
"""

from sqlalchemy.orm import Session

from src.models.user import User
from src.repositories.user_repo import update_user
from src.schemas.user import UpdateProfileRequest


def update_profile(db: Session, *, user: User, updates: UpdateProfileRequest) -> User:
    """
    Update user profile with validated fields.
    
    Flow:
    1. Check which fields are provided (not None)
    2. Update only those fields
    3. Save to DB
    4. Return updated user
    
    Security:
    - Only allows updating safe fields (name, bio)
    - Ignores attempts to update protected fields (handled by schema)
    """
    # Only update fields that are actually provided
    if updates.name is not None:
        user.name = updates.name
    
    if updates.bio is not None:
        user.bio = updates.bio
    
    # Save changes
    return update_user(db, user)
