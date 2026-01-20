from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to cans
    cans = relationship("Can", back_populates="owner", cascade="all, delete-orphan")

class Can(Base):
    __tablename__ = "cans"
    
    id = Column(Integer, primary_key=True, index=True)
    flavor = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    origin = Column(String(100), nullable=False)
    condition = Column(String(20), default="Good")
    description = Column(Text)
    image_path = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Foreign key to user
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationship to user
    owner = relationship("User", back_populates="cans")