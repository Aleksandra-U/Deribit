from fastapi import FastAPI

import asyncio

from app.exchange import get_data_minute

from app.client.router import router as router_deribit

app = FastAPI()

asyncio.ensure_future(get_data_minute())

app.include_router(router_deribit) 