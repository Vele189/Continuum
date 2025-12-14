from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.user import UserCreate, User
from app.services import user as user_service

router = APIRouter()

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
