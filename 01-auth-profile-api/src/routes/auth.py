"""
Auth routes.

Why:
- Routers let you keep endpoints organized by feature.
- /auth/register stays separate from /me routes etc.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.schemas.user import RegisterRequest, RegisterResponse, UserPublic
from src.services.auth_service import register_user, EmailAlreadyExists

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=RegisterResponse, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register endpoint.

    What happens here:
    - FastAPI already validated payload using RegisterRequest schema.
    - We call service to do logic + DB work.
    - We catch known error (email exists) and return clean HTTP error.
    """
    try:
        token, user = register_user(db, email=payload.email, password=payload.password, name=payload.name)
    except EmailAlreadyExists:
        # 409 Conflict = resource already exists
        raise HTTPException(status_code=409, detail="Email already registered")

    return RegisterResponse(
        access_token=token,
        user=UserPublic(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at,
            updated_at=user.updated_at,
        ),
    )
