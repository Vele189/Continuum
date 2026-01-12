from typing import Any

from app.api import deps
from app.core import security
from app.core.config import settings
from app.dbmodels import User
from app.schemas.user import PasswordResetConfirm, Token, TokenPayload, UserCreate, UserLogin
from app.services import user as user_service
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(
    user_in: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Register a new user.

    Creates a new user account and returns access and refresh tokens.
    """
    # Check if user already exists
    existing_user = user_service.get_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    # Create the user
    user = user_service.create(db, obj_in=user_in, background_tasks=background_tasks)

    # Generate tokens
    access_token = security.create_access_token({"sub": user.id})
    refresh_token = security.create_refresh_token({"sub": user.id})

    # Store refresh token in DB
    user_service.update_refresh_token(db, user, refresh_token)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }


@router.post("/login", response_model=Token)
def login(
    login_data: UserLogin,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Login with email and password (JSON body).

    Returns access token and refresh token.
    """
    user = user_service.authenticate(db, email=login_data.email, password=login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password"
        )

    access_token = security.create_access_token({"sub": user.id})
    refresh_token = security.create_refresh_token({"sub": user.id})

    # Store refresh token in DB
    user_service.update_refresh_token(db, user, refresh_token)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }


@router.post("/login/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login (form data).

    This endpoint is used by Swagger UI and OAuth2-compliant clients.
    Uses 'username' field for email (per OAuth2 spec).
    """
    user = user_service.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = security.create_access_token({"sub": user.id})
    refresh_token = security.create_refresh_token({"sub": user.id})

    # Store refresh token in DB
    user_service.update_refresh_token(db, user, refresh_token)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }


@router.post("/refresh-token", response_model=Token)
def refresh_access_token(
    refresh_token: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Refresh access token using a refresh token.
    """
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        token_data = TokenPayload(**payload)

        # Verify it's a refresh token
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )

    except (JWTError, ValidationError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        ) from exc

    user = db.query(User).filter(User.id == token_data.sub).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Validate token against stored token
    if user.refresh_token != refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    access_token = security.create_access_token({"sub": user.id})
    new_refresh_token = security.create_refresh_token({"sub": user.id})

    # Update stored refresh token
    user_service.update_refresh_token(db, user, new_refresh_token)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": new_refresh_token,
    }


@router.post("/password-recovery/{email}")
def recover_password(
    email: str, background_tasks: BackgroundTasks, db: Session = Depends(deps.get_db)
) -> dict:
    """
    Request password recovery.

    Sends a password reset token to the email if it exists.
    For security, always returns success even if email doesn't exist.
    """

    user_service.initiate_password_reset(db, email=email, background_tasks=background_tasks)
    return {"message": "If this email exists, a password reset token has been sent."}


@router.post("/reset-password")
def reset_password(
    data: PasswordResetConfirm,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Reset password using a reset token.
    """
    user = user_service.reset_password(db, token=data.token, new_password=data.new_password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token.",
        )
    return {"message": "Password updated successfully"}


@router.post("/logout")
def logout(
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Logout user by invalidating refresh token.

    Idempotent: can be called multiple times safely.
    """
    user_service.update_refresh_token(db, current_user, None)
    return {"message": "Logged out successfully"}
