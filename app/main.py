from fastapi import FastAPI
from .database import engine
from . import models
from .routes import products, orders

# Создание таблиц в базе данных
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

app = FastAPI()

# Подключение маршрутов
app.include_router(products.router)
app.include_router(orders.router)

# Создание таблиц при старте
@app.on_event("startup")
async def startup():
    await create_tables()
