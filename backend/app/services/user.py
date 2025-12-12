from typing import Optional
import uuid
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate

def get_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create(db: Session, obj_in: UserCreate) -> User:
    verification_token = str(uuid.uuid4())
    db_obj = User(
        email=obj_in.email,
        hashed_password=hash_password(obj_in.password),
        first_name=obj_in.first_name, 
        last_name=obj_in.last_name,
        role=obj_in.role,
        is_verified=False,
        verification_token=verification_token
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    
    # Mock sending email
    print(f"--- MOCK EMAIL ---")
    print(f"To: {obj_in.email}")
    print(f"Subject: Verify your email")
    print(f"Link: http://localhost:8000/api/v1/users/verify-email?token={verification_token}")
    print(f"------------------")
    
    return db_obj

def authenticate(db: Session, email: str, password: str) -> Optional[User]:
    user = get_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def update_refresh_token(db: Session, user: User, token: str) -> User:
    user.refresh_token = token
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_email(db: Session, token: str) -> Optional[User]:
    user = db.query(User).filter(User.verification_token == token).first()
    if not user:
        return None
    user.is_verified = True
    user.verification_token = None # Clear token after use
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def initiate_password_reset(db: Session, email: str) -> Optional[User]:
    user = get_by_email(db, email=email)
    if not user:
        return None
    
    reset_token = str(uuid.uuid4())
    user.password_reset_token = reset_token
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Mock sending email
    print(f"--- MOCK EMAIL ---")
    print(f"To: {email}")
    print(f"Subject: Reset your password")
    print(f"Token: {reset_token}")
    print(f"------------------")
    
    return user

def reset_password(db: Session, token: str, new_password: str) -> Optional[User]:
    user = db.query(User).filter(User.password_reset_token == token).first()
    if not user:
        return None
    
    user.hashed_password = hash_password(new_password)
    user.password_reset_token = None # Clear token
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
