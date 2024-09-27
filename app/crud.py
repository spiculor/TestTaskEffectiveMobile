from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError


# Функция для получения списка продуктов
async def get_products(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.Product).offset(skip).limit(limit))
    return result.scalars().all()

# Функция для получения продукта по ID
async def get_product(db: AsyncSession, product_id: int):
    return await db.get(models.Product, product_id)

# Функция для создания нового продукта
async def create_product(db: AsyncSession, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

# Функция для обновления информации о продукте
async def update_product(db: AsyncSession, product_id: int, product: schemas.ProductCreate):
    db_product = await get_product(db, product_id)
    if db_product is None:
        return None
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    await db.commit()
    await db.refresh(db_product)
    return db_product

# Функция для удаления продукта
async def delete_product(db: AsyncSession, product_id: int):
    db_product = await get_product(db, product_id)
    if db_product is None:
        return None
    await db.delete(db_product)
    await db.commit()
    return db_product

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

async def create_order(db: AsyncSession, order: schemas.OrderCreate):
    # Проверяем наличие всех товаров на складе до создания заказа
    for item in order.items:
        product = await get_product(db, item.product_id)
        if product.quantity_in_stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Недостаточно товара для продукта ID: {item.product_id}")
    
    # После успешной проверки создаем заказ
    db_order = models.Order()
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)

    # Добавляем товары в заказ и обновляем количество на складе
    for item in order.items:
        product = await get_product(db, item.product_id)
        product.quantity_in_stock -= item.quantity

        db_order_item = models.OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(db_order_item)

    # Подтверждаем изменения
    await db.commit()

    # Возвращаем созданный заказ
    await db.refresh(db_order)
    return db_order


# Получение списка заказов
async def get_orders(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.Order).offset(skip).limit(limit))
    return result.unique().scalars().all()

# Получение заказа по ID
async def get_order(db: AsyncSession, order_id: int):
    return await db.get(models.Order, order_id)

# Обновление статуса заказа
async def update_order_status(db: AsyncSession, order_id: int, status: schemas.OrderStatus):
    db_order = await get_order(db, order_id)
    if db_order is None:
        return None
    db_order.status = status
    await db.commit()
    await db.refresh(db_order)
    return db_order


# Отмена заказа с возвратом товара на склад
async def delete_order(db: AsyncSession, order_id: int):
    db_order = await get_order(db, order_id=order_id)
    
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    # Возвращаем товары на склад
    for item in db_order.items:
        db_product = await db.execute(select(models.Product).filter(models.Product.id == item.product_id))
        db_product = db_product.scalar_one_or_none()

        if db_product:
            db_product.quantity_in_stock += item.quantity
            await db.commit()

    # Удаляем сам заказ
    await db.delete(db_order)
    await db.commit()
    return db_order
