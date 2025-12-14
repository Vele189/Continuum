from typing import Any

from jose import jwt, JWTError
from pydantic import ValidationError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import deps
from app.core import security
from app.core.config import settings
from app.schemas.user import Token, UserLogin, TokenPayload, PasswordResetConfirm
from app.services import user as user_service
from app.models.user import User

router = APIRouter()

@router.post("/refresh-token", response_model=Token)
def refresh_access_token(
    refresh_token: str,  # pylint: disable=redefined-outer-name
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Refresh access token using a refresh token.
    """
    try:
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        # Verify it's a refresh token
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )

    except (JWTError, ValidationError) as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) from exc

    user = db.query(User).filter(User.id == token_data.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Validate token against stored token
    if user.refresh_token != refresh_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid refresh token",
        )

    access_token = security.create_access_token({"sub": str(user.id)})
    new_refresh_token = security.create_refresh_token({"sub": str(user.id)})

    # Update stored refresh token
    user_service.update_refresh_token(db, user, new_refresh_token)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": new_refresh_token,
    }

@router.post("/login", response_model=Token)
def login(
    login_data: UserLogin,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = user_service.authenticate(
        db, email=login_data.email, password=login_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = security.create_access_token({"sub": str(user.id)})
    new_refresh_token = security.create_refresh_token({"sub": str(user.id)})

    # Store refresh token in DB
    user_service.update_refresh_token(db, user, new_refresh_token)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": new_refresh_token,
    }

@router.post("/login/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = user_service.authenticate(
        db, email=form_data.username,  # OAuth2 spec uses 'username', mapping to email
        password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = security.create_access_token({"sub": str(user.id)})
    new_refresh_token = security.create_refresh_token({"sub": str(user.id)})

    # Store refresh token in DB
    user_service.update_refresh_token(db, user, new_refresh_token)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": new_refresh_token,
    }


@router.post("/password-recovery/{email}", response_model=dict)
def recover_password(email: str, db: Session = Depends(deps.get_db)) -> Any:
    """
    Password Recovery
    """
    user = user_service.initiate_password_reset(db, email=email)

    if not user:
        # Don't reveal if user exists or not for security
        # But for this task/development, let's just return success anyway
        pass

    return {"message": "If this email exists, a password reset token has been sent."}


@router.post("/reset-password", response_model=dict)
def reset_password(
    data: PasswordResetConfirm,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Reset Password
    """
    user = user_service.reset_password(
        db, token=data.token, new_password=data.new_password
    )
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired token.",
        )
    return {"message": "Password updated successfully"}
