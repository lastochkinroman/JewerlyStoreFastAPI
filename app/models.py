from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key = True, index = True)
    article = Column(String, unique = True, index = True)
    name = Column(String)
    metal = Column(String)
    probe = Column(Integer)
    weight = Column(Float)
    price = Column(Float)
    size = Column(Float, nullable=True)

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key = True, index = True)
    full_name = Column(String)
    phone = Column(String, unique=True, index=True)
    email = Column(String, nullable = True)
    created_at = Column(DateTime, default = datetime.utcnow)