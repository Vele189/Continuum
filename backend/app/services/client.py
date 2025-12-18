from typing import Optional, List
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.database import Client
from app.schemas.client import ClientCreate, ClientUpdate


def create(db: Session, obj_in: ClientCreate, created_by: Optional[int] = None) -> Client:
    """Create a new client"""
    db_obj = Client(
        name=obj_in.name,
        email=obj_in.email,
        created_by=created_by
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get(db: Session, client_id: int) -> Optional[Client]:
    """Retrieve a client by ID"""
    return db.query(Client).filter(Client.id == client_id).first()


def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Client]:
    """List all clients with pagination"""
    return db.query(Client).offset(skip).limit(limit).all()


def update(db: Session, client: Client, obj_in: ClientUpdate) -> Client:
    """Update a client"""
    update_data = obj_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(client, field, value)
    
    # Manually update updated_at since SQLite doesn't support onupdate triggers
    client.updated_at = datetime.now(timezone.utc)
    
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def delete(db: Session, client_id: int) -> Optional[Client]:
    """Delete a client"""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        return None
    
    db.delete(client)
    db.commit()
    return client


