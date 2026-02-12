from typing import Optional, List

from pydantic import BaseModel, ConfigDict, EmailStr, Field



class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str
    role: Optional[str] = "user"
    signup_code: Optional[str] = None
    documents: Optional[List[str]] = None


class SignupCodeRequest(BaseModel):
    email: EmailStr

class UserLogin(BaseModel):
    email: str
    password: str


class ForgotPasswordRequest(BaseModel):
    email: str


class LoginWithCode(BaseModel):
    email: str
    code: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str
    seller_verified: bool

    model_config = ConfigDict(from_attributes=True)


class AdminUserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str
    seller_verified: bool
    documents: Optional[List[str]] = None

    model_config = ConfigDict(from_attributes=True)


class AdminSellerDocumentsOut(BaseModel):
    user_id: int = Field(alias="userId")
    username: str
    email: str
    documents: List[str]

    model_config = ConfigDict(populate_by_name=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    role: str
    seller_verified: bool


class WatchBase(BaseModel):
    name: str
    brand: str
    price: float
    description: str
    tags: Optional[str] = None
    image_url: Optional[str] = Field(default=None, alias="imageUrl")
    seller_id: Optional[int] = Field(default=None, alias="sellerId")

    model_config = ConfigDict(populate_by_name=True)


class WatchCreate(WatchBase):
    pass


class WatchUpdate(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    tags: Optional[str] = None
    image_url: Optional[str] = Field(default=None, alias="imageUrl")
    seller_id: Optional[int] = Field(default=None, alias="sellerId")
    status: Optional[str] = None
    approved_by: Optional[int] = Field(default=None, alias="approvedBy")

    model_config = ConfigDict(populate_by_name=True)


class WatchOut(WatchBase):
    id: int
    status: str
    approved_by: Optional[int] = Field(default=None, alias="approvedBy")
    seller_name: Optional[str] = Field(default=None, alias="sellerName")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class WishlistResponse(BaseModel):
    wishlist: list[WatchOut]


class PromotionCreate(BaseModel):
    title: str
    description: str
    watch_id: int = Field(alias="watchId")
    discount: Optional[str] = None
    valid_until: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class PromotionOut(PromotionCreate):
    id: int
    seller_id: int
