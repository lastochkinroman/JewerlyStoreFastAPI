from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ItemBase(BaseModel):
    article: str
    name: str
    metal: str
    probe: int
    weight: float
    price: float
    size: Optional[float] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    class Config:
        from_attributes = True

class CustomerBase(BaseModel):
    full_name: str
    phone: str
    email: Optional[EmailStr] = None

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True