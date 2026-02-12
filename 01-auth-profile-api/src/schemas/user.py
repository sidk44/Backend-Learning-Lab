"""
Pydantic schemas for User-related API responses/requests.

Why:
- Prevents leaking DB-only fields (like password_hash).
- Provides automatic input validation (email format, min lengths, etc.).
- Gives clean response models for clients (frontend/Postman).
"""

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


def user_to_public(user) -> "UserPublic":
    """
    Helper to convert SQLAlchemy User model to UserPublic schema.
    
    Why:
    - Avoids repeating the same mapping code everywhere.
    - One place to maintain if we add/remove fields.
    """
    return UserPublic(
        id=user.id,
        email=user.email,
        name=user.name,
        bio=user.bio,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


class UserPublic(BaseModel):
    """
    What we send back to the client about a user.

    Notice:
    - No password field here.
    - This is intentional: password_hash should never be returned.
    """
    id: UUID
    email: EmailStr
    name: str
    bio: str | None = None
    created_at: datetime
    updated_at: datetime


class RegisterRequest(BaseModel):
    """
    What client must send to register.

    EmailStr:
    - automatically validates correct email format.

    Field(...):
    - adds extra validation rules and readable docs in Swagger.
    """
    email: EmailStr
    password: str = Field(min_length=6, max_length=64)
    name: str = Field(min_length=2, max_length=120)
    

class RegisterResponse(BaseModel):
    """
    What we return after registering.

    We include:
    - token: so user can immediately call protected APIs
    - user: basic public info
    """
    access_token: str
    token_type: str = "bearer"
    user: UserPublic


class LoginRequest(BaseModel):
    """
    What client sends to login.
    
    Simple:
    - email + password only
    """
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """
    What we return after successful login.
    
    Same as register response:
    - token for authorization
    - user info
    """
    access_token: str
    token_type: str = "bearer"
    user: UserPublic


class UpdateProfileRequest(BaseModel):
    """
    What client can send to update profile.
    
    Why all optional:
    - User can update just name, or just bio, or both.
    - PATCH is for partial updates.
    
    Security:
    - We don't allow updating email, password, or id here.
    - Those require separate secure flows.
    """
    name: str | None = Field(None, min_length=2, max_length=120)
    bio: str | None = Field(None, max_length=500)
