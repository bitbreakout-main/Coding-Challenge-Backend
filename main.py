# main.py
from fastapi import FastAPI, WebSocket
import ccxt.async_support as ccxt
import redis.asyncio as redis
from pydantic import BaseModel
import asyncio

app = FastAPI()
exchange = ccxt.binance()
r = redis.from_url("redis://localhost:6379")

class MarketOrder(BaseModel):
    side: str  # "buy" or "sell"
    amount: float

@app.on_event("startup")
async def start_depth_updater():
    asyncio.create_task(update_depth())

@app.websocket("/ws/depth")
async def depth_websocket(websocket: WebSocket):
    await websocket.accept()
    # send initial + listen to pubsub
    pass

@app.post("/market")
async def execute_market(order: MarketOrder):
    # walk order book, return fill
    pass

async def update_depth():
    while True:
        orderbook = await exchange.fetch_order_book("BTC/USDT", limit=20)
        # store in Redis + publish
        await asyncio.sleep(2)
