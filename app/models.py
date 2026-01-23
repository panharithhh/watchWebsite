from operator import index
from sqlalchemy import Column, Integer, Nullable, String, Float, Text, DateTime, ForeignKey, Enum, false, Numeric
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import relationship
import enum

class UserRole(str, enum.Enum):
    buyer = "buyer"
    seller = "seller"
    admin = "admin"


class WatchStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class PaymentStatus(str, enum.Enum):
    paid = "paid"
    unpaid = "unpaid"

class PaymentMethod(str, enum.Enum):
    cash = "cash"
    card = "card"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index = True)
    email = Column(String(100), unique=True, nullable=False,index = True)
    password_hash = Column(Text, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.buyer)

class Watch(Base):
    __tablename__ = "watches"
    
    id = Column(Integer, primary_key=True, index = True)
    name = Column(String(50), nullable= False)
    brand = Column(String(50), nullable=False)
    price = Column(Numeric(12,2), nullable= False)
    description = Column(String(50), nullable=False)
    tags = Column(String)
    image_url = Column(String)

    
    status = Column(Enum(WatchStatus), nullable =False, default=WatchStatus.pending)
    seller_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    discount_percent = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    watch_id = Column(Integer, ForeignKey("watches.id", ondelete="CASCADE"), nullable=False)


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    total_amount = Column(Numeric(12, 2), nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    payment_status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.unpaid)
    created_at = Column(DateTime, nullable=False, default=func.now())


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    watch_id = Column(Integer, ForeignKey("watches.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
    line_total = Column(Numeric(12, 2), nullable=False)


class WishlistItem(Base):
    __tablename__ = "wishlist_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    watch_id = Column(Integer, ForeignKey("watches.id", ondelete="CASCADE"), nullable=False)


class BrandPreference(Base):
    __tablename__ = "brand_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    brand = Column(String(50), nullable=False)
    search_count = Column(Integer, nullable=False, default=0)
