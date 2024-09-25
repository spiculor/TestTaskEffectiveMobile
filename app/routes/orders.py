from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter()

# Эндпоинт для создания нового заказа
@router.post("/orders/", response_model=schemas.Order)
async def create_order(order: schemas.OrderCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_order(db=db, order=order)

# Эндпоинт для получения списка заказов
@router.get("/orders/", response_model=List[schemas.Order])
async def read_orders(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.get_orders(db, skip=skip, limit=limit)

# Эндпоинт для получения заказа по ID
@router.get("/orders/{order_id}", response_model=schemas.Order)
async def read_order(order_id: int, db: AsyncSession = Depends(get_db)):
    db_order = await crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

# Эндпоинт для обновления статуса заказа
@router.patch("/orders/{order_id}/status", response_model=schemas.Order)
async def update_order_status(order_id: int, status: schemas.OrderStatus, db: AsyncSession = Depends(get_db)):
    db_order = await crud.update_order_status(db, order_id=order_id, status=status)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

# Эндпоинт для удаления заказа
@router.delete("/orders/{order_id}", response_model=schemas.Order)
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)):
    db_order = await crud.delete_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order
