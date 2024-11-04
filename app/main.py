from fastapi import FastAPI, Request

import asyncio

from app.exchange import get_data_minute
from contextlib import asynccontextmanager
from app.client.router import router as router_deribit

import time 

from app.logger import logger





@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.ensure_future(get_data_minute()) #создаю задачу
    yield
    # Здесь вы можете добавить логику для корректного завершения фоновой задачи 
    task.cancel()  # Отменяем задачу 
    try: 
        await task  # Ожидаем завершение задачи 
    except asyncio.CancelledError: 
        pass  # Игнорируем отмену


app = FastAPI(lifespan=lifespan)





app.include_router(router_deribit) 