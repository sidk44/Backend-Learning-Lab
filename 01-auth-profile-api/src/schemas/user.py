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
