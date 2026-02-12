"""
Auth routes.

Why:
- Routers let you keep endpoints organized by feature.
- /auth/register stays separate from /me routes etc.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.schemas.user import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse, user_to_public
from src.services.auth_service import register_user, login_user, EmailAlreadyExists, InvalidCredentials

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
        user=user_to_public(user),
    )


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """
    Login endpoint.
    
    What happens:
    - Verify email + password
    - Return JWT token + user info
    
    Security:
    - 401 Unauthorized if credentials are wrong
    - Don't reveal whether email or password is incorrect
    """
    try:
        token, user = login_user(db, email=payload.email, password=payload.password)
    except InvalidCredentials:
        # 401 Unauthorized = authentication failed
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return LoginResponse(
        access_token=token,
        user=user_to_public(user),
    )
