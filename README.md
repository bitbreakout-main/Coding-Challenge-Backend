# BitBreakout Backend Challenge

Time: Limit: 2 hours  
Submit: GitHub repo link + live WebSocket + `curl` test
Stack: FastAPI + CCXT + Redis + WebSockets + Pydantic

---

## Task: Real-Time Order Book + Market Order with Slippage

### Goal
Simulate Binance BTC/USDT order book in Redis,  
expose live depth via WebSocket,  
and execute market orders with slippage.

---

### Requirements
#### 1. Background Updater (`/start`)
- Fetch BTC/USDT order book (depth 20) every 2 seconds
- Store bids/asks in Redis sorted sets:
  ```redis
  bids:price:user123 -> 103200.0
  asks:price:user456 -> 103210.5
  ```
- Publish snapshot to Redis channel `depth:update`

#### 2. WebSocket `/ws/depth`
- On connect: send current top 10 bids/asks
- On update: push delta (only changed levels)
  ```json
  {"bids": [[103200, 1.5]], "asks": [[103210, 0.8]]}
  ```

#### 3. POST `/market`
```bash
curl -X POST http://localhost:8000/market \
  -d '{"side": "buy", "amount": 0.5}'
```
- Walk the asks (from Redis)
 irland- Calculate average fill price + slippage %
- Return:
  ```json
  {
    "filled": 6.5,
    "avg_price": 103225.3,
    "slippage_pct": 0.24,
    "status": "filled"
  }
  ```

---

## How to Run

```bash
docker-compose up --build
```

### Test WebSocket
```bash
wscat -c ws://localhost:8000/ws/depth
```

### Test Market Order
```bash
curl -X POST http://localhost:8000/market \
  -H "Content-Type: application/json" \
  -d '{"side": "buy", "amount": 0.5}'
```

---
