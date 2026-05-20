# RealMarketAPI Python SDK (Beta)

Beta Python client for RealMarketAPI REST and WebSocket endpoints.

## Install

```bash
pip install realmarketapi-python-sdk-beta
```

## REST quick start

```python
from realmarketapi_sdk import RealMarketApiClient

client = RealMarketApiClient(api_key="YOUR_API_KEY")
price = client.get_price("EURUSD", "M1")
print(price["closePrice"])
client.close()
```

## WebSocket quick start

```python
import asyncio
from realmarketapi_sdk import RealMarketApiWebSocket

ws = RealMarketApiWebSocket(api_key="YOUR_API_KEY")

async def main() -> None:
    async for tick in ws.stream_price("BTCUSDT", "M1"):
        print(tick)

asyncio.run(main())
```

## Beta scope
- REST: price, candles, history, symbols, SMA.
- WebSocket: price and candles with reconnect loop.
- Additive API expansion planned prior to stable 1.0.
