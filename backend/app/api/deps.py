from typing import Generator, Optional

from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal
from app.dbmodels import Project, ProjectMember, User, UserRole, Client
from app.schemas.user import TokenPayload
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login/access-token")


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, #CHANGED FROM 403 TO 401
            detail="Could not validate credentials",
        ) from exc
    user = db.query(User).filter(User.id == token_data.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_user_optional(
    db: Session = Depends(get_db),
    token: str = Depends(
        OAuth2PasswordBearer(
            tokenUrl=f"{settings.API_V1_STR}/auth/login/access-token", auto_error=False
        )
    ),
) -> Optional[User]:
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        token_data = TokenPayload(**payload)
        user = db.query(User).filter(User.id == token_data.sub).first()
        return user
    except (JWTError, ValidationError):
        return None


def get_current_active_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Verify the current user has admin privileges.
    Admin roles: ADMIN, PROJECTMANAGER
    """
    admin_roles = {UserRole.ADMIN, UserRole.PROJECTMANAGER}
    if current_user.role not in admin_roles:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    return current_user


def is_admin_user(user: User) -> bool:
    """Helper function to check if a user has admin privileges."""
    return user.role in {UserRole.ADMIN, UserRole.PROJECTMANAGER}


# ==================================================get the current memebr of a project==========================
def get_current_project_member(
    project_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> ProjectMember:
    """Helper function to check if the current user is a member of the project and get that member."""
    # first we need to check if the project exists if not we return an error
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="This Project does not exist")
    # then we need to check if the current user is a member of the project
    # if it does exist if not we return an error
    member = (
        db.query(ProjectMember)
        .filter(ProjectMember.project_id == project_id, ProjectMember.user_id == current_user.id)
        .first()
    )
    if not member:
        raise HTTPException(status_code=403, detail="You are not a member of this project")
    # then we return the member
    return member


# ==================================================get the current admin of a project==========================
def get_current_project_admin(
    project_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> ProjectMember:
    """Helper function to check if the current user is an admin or project manager of the project."""

    # we need to check if the project exists if not we return an error
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="This Project does not exist")

    # then we check if the current user is an admin of the project
    # if not we check if they are a project manager
    admin = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == current_user.id,
            ProjectMember.role == UserRole.ADMIN.value,
        )
        .first()
    )
    if admin:
        return admin

    # then we check if the current user is a project manager(member)
    # of the project if not we return an error
    member = get_current_project_member(project_id, current_user, db)
    # then we check if the member has project manager role
    if member.role == UserRole.PROJECTMANAGER.value:
        return member

    # if neither admin nor project manager we return an error
    raise HTTPException(
        status_code=403, detail="You must be an admin or a project manager of this project"
    )

#Matches PM mental model
def get_current_client(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Client:
    client = (
        db.query(Client)
        .filter(Client.created_by == user.id)
        .first()
    )

    if not client:
        raise HTTPException(
            status_code=403,
            detail="User is not associated with any client",
        )

    return client

#ADD FUNCTION FOR GETTING CURRENT CLIENT. 
#ADD FUNCTION FOR GETTING LIST OF CLIENTS. Done but doesnt work for the current model
#ADD ENDPOINT FOR POST MAN TESTING LIKE A JSON TEMPLATE POSTMAN COLLECTION