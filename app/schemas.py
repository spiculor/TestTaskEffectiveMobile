from pydantic import BaseModel
from typing import List
from datetime import datetime
import enum

# Схема для создания нового продукта
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    quantity_in_stock: int

    class Config:
        orm_mode = True  

# Схема для возврата данных о продукте
class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity_in_stock: int

class OrderStatus(str, enum.Enum):
    processing = "в процессе"
    shipped = "отправлен"
    delivered = "доставлен"

# Схема для создания элемента заказа (OrderItem)
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

# Схема для создания заказа
class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

# Схема для возврата информации о заказе
class OrderItem(BaseModel):
    product_id: int
    quantity: int

    class Config:
        orm_mode = True

class Order(BaseModel):
    id: int
    created_at: datetime
    status: OrderStatus
    items: List[OrderItem]

    class Config:
        orm_mode = True


class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True