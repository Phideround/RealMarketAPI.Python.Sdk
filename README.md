# RealMarketAPI Python SDK (Beta)

Official beta Python SDK for RealMarketAPI REST and WebSocket market data endpoints.

Website: [https://realmarketapi.com/](https://realmarketapi.com/)

## Why use this SDK

- Thin Python wrapper for RealMarketAPI HTTP and streaming APIs.
- Simple class-based client for request/response usage.
- Async WebSocket streams with automatic reconnect behavior.
- Small dependency footprint (`httpx`, `websockets`).

## Requirements

- Python 3.9+
- RealMarketAPI API key

## Install

```bash
pip install realmarketapi-python-sdk-beta
```

## Quick start

### REST client

```python
from realmarketapi_sdk import RealMarketApiClient

client = RealMarketApiClient(api_key="YOUR_API_KEY")

try:
    price = client.get_price("EURUSD", "M1")
    print("Close:", price.get("closePrice"))
finally:
    client.close()
```

### WebSocket client

```python
import asyncio
from realmarketapi_sdk import RealMarketApiWebSocket

ws = RealMarketApiWebSocket(api_key="YOUR_API_KEY")

async def main() -> None:
    async for tick in ws.stream_price("BTCUSDT", "M1"):
    print(tick)

asyncio.run(main())
```

## REST API methods

All REST methods return a Python `dict` parsed from JSON and include your API key as query parameter.

### `get_price(symbol_code, time_frame)`

Example:

```python
price = client.get_price("EURUSD", "M1")
```

Example response payload:

```json
{
    "symbolCode": "EURUSD",
    "timeFrame": "M1",
    "openPrice": 1.07874,
    "highPrice": 1.07882,
    "lowPrice": 1.07868,
    "closePrice": 1.07879,
    "openTime": "2026-05-21T09:12:00Z"
}
```

### `get_candles(symbol_code, time_frame)`

Example:

```python
candles = client.get_candles("BTCUSDT", "M5")
```

Example response payload:

```json
{
    "symbolCode": "BTCUSDT",
    "timeFrame": "M5",
    "candles": [
        {
            "openTime": "2026-05-21T09:10:00Z",
            "openPrice": 68620.3,
            "highPrice": 68690.1,
            "lowPrice": 68588.7,
            "closePrice": 68655.8,
            "volume": 128.42
        }
    ]
}
```

### `get_history(symbol_code, start_time, end_time, page_number=1, page_size=20)`

Example:

```python
history = client.get_history(
    symbol_code="EURUSD",
    start_time="2026-05-20T00:00:00Z",
    end_time="2026-05-21T00:00:00Z",
    page_number=1,
    page_size=20,
)
```

Example response payload:

```json
{
    "pageNumber": 1,
    "pageSize": 20,
    "totalPages": 14,
    "items": [
        {
            "openTime": "2026-05-20T00:00:00Z",
            "openPrice": 1.07913,
            "highPrice": 1.07942,
            "lowPrice": 1.07898,
            "closePrice": 1.07920,
            "volume": 241.11
        }
    ]
}
```

### `get_symbols()`

Example:

```python
symbols = client.get_symbols()
```

Example response payload:

```json
{
    "symbols": ["EURUSD", "BTCUSDT", "XAUUSD"]
}
```

### `get_sma(symbol_code, time_frame, period=20)`

Example:

```python
sma = client.get_sma("EURUSD", "M15", period=50)
```

Example response payload:

```json
{
    "symbolCode": "EURUSD",
    "timeFrame": "M15",
    "period": 50,
    "value": 1.08024,
    "openTime": "2026-05-21T09:00:00Z"
}
```

## WebSocket streaming methods

The WebSocket client exposes async generators and reconnects after transient failures.

### `stream_price(symbol_code, time_frame)`

Example:

```python
async for event in ws.stream_price("EURUSD", "M1"):
    print(event)
```

Example message payload:

```json
{
    "symbolCode": "EURUSD",
    "timeFrame": "M1",
    "closePrice": 1.07879,
    "openTime": "2026-05-21T09:12:00Z"
}
```

### `stream_candles(symbol_code, time_frame)`

Example:

```python
async for event in ws.stream_candles("BTCUSDT", "M5"):
    print(event)
```

Example message payload:

```json
{
    "symbolCode": "BTCUSDT",
    "timeFrame": "M5",
    "openTime": "2026-05-21T09:10:00Z",
    "openPrice": 68620.3,
    "highPrice": 68690.1,
    "lowPrice": 68588.7,
    "closePrice": 68655.8,
    "volume": 128.42
}
```

## Error handling notes

- REST methods call `response.raise_for_status()`, so HTTP 4xx/5xx responses raise `httpx.HTTPStatusError`.
- WebSocket streams retry on connection errors using `reconnect_delay_seconds` (default `2.0`).
- Cancel the async task to stop streaming cleanly.

## Beta scope and compatibility

- Current REST coverage: price, candles, history, symbols, SMA.
- Current WebSocket coverage: price and candles.
- This package is beta and may receive additive changes before stable `1.0`.

## Links

- RealMarketAPI homepage: [https://realmarketapi.com/](https://realmarketapi.com/)
