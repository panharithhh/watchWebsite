from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    buyer = "buyer"
    seller = "seller"
    admin = "admin"

class WatchStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class PaymentStatus(str, Enum):
    paid = "paid"
    unpaid = "unpaid"

class PaymentMethod(str, Enum):
    cash = "cash"
    card = "card"

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password_hash: str
    role: Optional[UserRole] = None

class UserOut(UserBase):
    id: int
    role: UserRole

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email : EmailStr
    password_hash : str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class LoginWithCode(BaseModel):
    email: EmailStr
    code: str

class AdminAction(BaseModel):
    admin_id: int

class SellerUpdate(BaseModel):
    admin_id: int
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None

class AdminWatchUpdate(BaseModel):
    admin_id: int
    name: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[Decimal] = None
    description: Optional[str] = None
    tags: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[WatchStatus] = None

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


class WatchUpdate(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[Decimal] = None
    description: Optional[str] = None
    tags: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[WatchStatus] = None

class WatchSearch(BaseModel):
    name: Optional[str] = None
    tags: Optional[str] = None
    brand: Optional[str] = None

class WatchApproval(BaseModel):
    admin_id: int
    status: WatchStatus

class BrandBase(BaseModel):
    name: str

class BrandCreate(BrandBase):
    pass

class BrandUpdate(BaseModel):
    name: Optional[str] = None

class BrandOut(BrandBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class PromotionCreate(BaseModel):
    title: str
    discount_percent: int
    start_date: datetime
    end_date: datetime
    watch_id: int

class PromotionOut(PromotionCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

class OrderItemCreate(BaseModel):
    watch_id: int
    quantity: int = 1

class CartTotalRequest(BaseModel):
    items: list[OrderItemCreate]

class CartItemOut(BaseModel):
    watch_id: int
    quantity: int
    unit_price: Decimal
    line_total: Decimal

class OrderCreate(BaseModel):
    buyer_id: int
    payment_method: PaymentMethod
    items: list[OrderItemCreate]

class OrderItemOut(BaseModel):
    id: int
    watch_id: int
    quantity: int
    unit_price: Decimal
    line_total: Decimal

    model_config = ConfigDict(from_attributes=True)

class OrderOut(BaseModel):
    id: int
    buyer_id: int
    total_amount: Decimal
    payment_method: PaymentMethod
    payment_status: PaymentStatus
    created_at: datetime
    items: list[OrderItemOut]

    model_config = ConfigDict(from_attributes=True)

class CartTotalOut(BaseModel):
    total_amount: Decimal
    items: list[CartItemOut]

class RevenueOut(BaseModel):
    total_revenue: Decimal

class WishlistItemCreate(BaseModel):
    user_id: int
    watch_id: int

class WishlistItemOut(BaseModel):
    id: int
    user_id: int
    watch_id: int

    model_config = ConfigDict(from_attributes=True)

class BrandSearchTrack(BaseModel):
    user_id: int
    brand: str

class BrandPreferenceOut(BaseModel):
    id: int
    user_id: int
    brand: str
    search_count: int

    model_config = ConfigDict(from_attributes=True)

class RecommendedOut(BaseModel):
    watch_id: int
    score: int
