from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# User schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str

# Can schemas
class CanCreate(BaseModel):
    flavor: str
    type: str
    year: int
    condition: str = "Good"
    description: Optional[str] = None

class CanResponse(BaseModel):
    id: int
    flavor: str
    type: str
    year: int
    origin: str
    condition: str
    description: Optional[str]
    image_path: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True