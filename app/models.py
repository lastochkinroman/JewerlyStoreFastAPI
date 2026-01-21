from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from datetime import datetime
from .database import Base
from sqlalchemy.orm import relationship

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

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    sale_price = Column(Float)
    sold_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer")
    item = relationship("item")


class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)