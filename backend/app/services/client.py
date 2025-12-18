from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.database import Client, User
from app.schemas.client import ClientCreate, ClientUpdate

class ClientService:
    @staticmethod
    def create_client(db: Session, client_in: ClientCreate, current_user_id: Optional[int] = None) -> Client:
        # Check if client with same name already exists
        existing = db.query(Client).filter(Client.name == client_in.name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Client with this name already exists"
            )
        
        db_client = Client(
            name=client_in.name,
            email=client_in.email,
            created_by=current_user_id
        )
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        return db_client

    @staticmethod
    def list_clients(db: Session, skip: int = 0, limit: int = 100) -> List[Client]:
        return db.query(Client).offset(skip).limit(limit).all()

    @staticmethod
    def get_client(db: Session, client_id: int) -> Optional[Client]:
        return db.query(Client).filter(Client.id == client_id).first()

    @staticmethod
    def update_client(db: Session, client_id: int, client_in: ClientUpdate) -> Client:
        db_client = ClientService.get_client(db, client_id)
        if not db_client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
        
        update_data = client_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_client, field, value)
            
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        return db_client

    @staticmethod
    def delete_client(db: Session, client_id: int) -> Client:
        db_client = ClientService.get_client(db, client_id)
        if not db_client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
        
        db.delete(db_client)
        db.commit()
        return db_client
