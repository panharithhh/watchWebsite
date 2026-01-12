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
