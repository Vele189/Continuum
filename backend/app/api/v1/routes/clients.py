from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.database import User
from app.schemas.client import Client, ClientCreate
from app.services.client import ClientService
from app.api import deps
from typing import Optional

router = APIRouter()

@router.post("/", response_model=Client, status_code=status.HTTP_201_CREATED)
def create_client(
    client_in: ClientCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(deps.get_current_user_optional),
):
    """
    Create a new client.
    """
    user_id = current_user.id if current_user else None
    return ClientService.create_client(db, client_in, user_id)

@router.get("/", response_model=List[Client])
def list_clients(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    List clients.
    """
    return ClientService.list_clients(db, skip=skip, limit=limit)

