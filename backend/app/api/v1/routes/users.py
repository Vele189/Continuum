from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.user import UserCreate, User
from app.services import user as user_service
from app.database import User as UserModel

router = APIRouter()

@router.get("/me", response_model=User)
def get_current_user_profile(
    current_user: UserModel = Depends(deps.get_current_user),
):
    """
    Get current authenticated user's profile.
    
    Returns the full user profile for the currently authenticated user.
    No user ID is required - the user is identified from the JWT token.
    """
    return current_user


@router.post("/", response_model=User)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(deps.get_db),
):
    """
    Create new user.
    """
    user = user_service.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = user_service.create(db, obj_in=user_in)
    return user


@router.get("/verify-email")
def verify_email(
    token: str,
    db: Session = Depends(deps.get_db),
):
    """
    Verify user email.
    """
    user = user_service.verify_email(db, token=token)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid verification token.",
        )
    return {"message": "Email verified successfully"}
