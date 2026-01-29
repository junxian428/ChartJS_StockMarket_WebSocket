import asyncio
import json
import random
import time
import websockets

URI = "ws://localhost:8765"

async def send_candles():
    price = 100.00
    volatility = 0.002      # 0.2% max move per candle
    wick_range = 0.001      # wick size

    async with websockets.connect(URI) as ws:
        while True:
            open_price = price

            # small near-range move
            change_pct = random.uniform(-volatility, volatility)
            close_price = open_price * (1 + change_pct)

            # realistic wicks
            high_price = max(open_price, close_price) * (1 + random.uniform(0, wick_range))
            low_price = min(open_price, close_price) * (1 - random.uniform(0, wick_range))

            candle = {
                "time": int(time.time()),
                "open": round(open_price, 2),
                "high": round(high_price, 2),
                "low": round(low_price, 2),
                "close": round(close_price, 2)
            }

            await ws.send(json.dumps(candle))
            price = close_price

            await asyncio.sleep(1)

asyncio.run(send_candles())
