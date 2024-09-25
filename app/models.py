from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
import enum

# Перечисление для статусов заказа
class OrderStatus(enum.Enum):
    processing = "в процессе"
    shipped = "отправлен"
    delivered = "доставлен"

# Модель для товаров
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    quantity_in_stock = Column(Integer)


# Модель для заказа
class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(OrderStatus, native_enum=False), default=OrderStatus.processing)  

    items = relationship("OrderItem", back_populates="order", lazy="joined")


# Модель для элементов заказа
class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

    order = relationship("Order", back_populates="items", lazy="joined")
    product = relationship("Product", lazy="joined")
