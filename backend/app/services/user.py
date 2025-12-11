from typing import Optional
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate

def get_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create(db: Session, obj_in: UserCreate) -> User:
    db_obj = User(
        email=obj_in.email,
        hashed_password=hash_password(obj_in.password),
        first_name=obj_in.first_name, 
        last_name=obj_in.last_name,
        role=obj_in.role,
        is_verified=False
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def authenticate(db: Session, email: str, password: str) -> Optional[User]:
    user = get_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
