from enum import Enum as PyEnum

from sqlalchemy import Boolean, Column, Float, Integer, String, Text, DateTime, func, Numeric, UniqueConstraint
from sqlalchemy import Enum as SAEnum
from database import Base


class UserRole(str, PyEnum):
    buyer = "buyer"
    seller = "seller"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(SAEnum(UserRole, name = "user_role"), nullable=False, default=UserRole.buyer.value)
    seller_verified = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class SellerDocument(Base):
    __tablename__ = "seller_documents"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    data_url = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Watch(Base):
    __tablename__ = "watches"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    brand = Column(String(50), nullable=False)
    price = Column(Numeric(12, 2), nullable=False)
    description = Column(String(50), nullable=False)
    tags = Column(String, nullable=True)
    image_url = Column("image_url", String, nullable=True)
    status = Column(SAEnum("pending", "approved", "rejected", name="watchstatus"), nullable=False, default="pending")
    seller_id = Column("seller_id", Integer, nullable=False)
    approved_by = Column("approved_by", Integer, nullable=True)


Watches = Watch


class WishlistItem(Base):
    __tablename__ = "wishlist"
    __table_args__ = (UniqueConstraint("user_id", "watch_id", name="wishlist_user_watch_key"),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    watch_id = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
