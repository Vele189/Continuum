from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api import deps
from app.database import User
from app.schemas.client import Client, ClientCreate, ClientUpdate
from app.services import client as client_service
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/", response_model=Client, status_code=status.HTTP_201_CREATED)
def create_client(
    client_in: ClientCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin),
):
    """
    Create a new client.

    Requires admin privileges (ADMIN or PROJECTMANAGER role).
    """
    try:
        client = client_service.create(
            db=db,
            obj_in=client_in,
            created_by=current_user.id
        )
        return client
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e


@router.get("/", response_model=List[Client])
def list_clients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin),
):
    """
    List all clients.

    Requires admin privileges.
    Supports pagination via skip and limit query parameters.
    """
    clients = client_service.get_all(db=db, skip=skip, limit=limit)
    return clients


@router.get("/{client_id}", response_model=Client)
def get_client(
    client_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin),
):
    """
    Get client details by ID.

    Requires admin privileges.
    """
    client = client_service.get(db=db, client_id=client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    return client


@router.put("/{client_id}", response_model=Client)
def update_client(
    client_id: int,
    client_in: ClientUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin),
):
    """
    Update a client.

    Requires admin privileges.
    Only provided fields will be updated.
    """
    client = client_service.get(db=db, client_id=client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )

    try:
        updated_client = client_service.update(
            db=db,
            client=client,
            obj_in=client_in
        )
        return updated_client
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_client(
    client_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin),
):
    """
    Delete a client.

    Requires admin privileges.
    """
    client = client_service.delete(db=db, client_id=client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
