from datetime import datetime

from pydantic import BaseModel

from uuid import UUID

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: UUID
    email: str
    created_at: datetime

    class Config:
        from_attributes = True