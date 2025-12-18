from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

# Shared properties
class ClientBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None

# Properties to receive on creation
class ClientCreate(ClientBase):
    pass

# Properties to receive on update
class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

# Properties shared by models stored in DB
class ClientInDBBase(ClientBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_by: Optional[int] = None
    created_at: datetime

# Properties to return to client
class Client(ClientInDBBase):
    pass
