from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional
from decimal import Decimal
from enum import Enum

class UserRole(str, Enum):
    buyer = "buyer"
    seller = "seller"
    admin = "admin"

class WatchStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password_hash: str

class UserOut(UserBase):
    id: int
    role: UserRole

    model_config = ConfigDict(from_attributes=True)

class WatchBase(BaseModel):
    name: str = Field(..., max_length=100)
    brand: Optional[str] = Field(None, max_length=50)
    price: Decimal
    description: Optional[str] = None
    tags: Optional[str] = None
    image_url: Optional[str] = None

class WatchCreate(WatchBase):
    seller_id: int

class WatchOut(WatchBase):
    id: int
    status: WatchStatus
    seller_id: int
    approved_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
