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
    "openPrice": 1.07874,
    "highPrice": 1.07882,
    "lowPrice": 1.07868,
    "closePrice": 1.07879,
    "volume": 152.0,
    "openTime": "2026-05-21T09:12:00Z",
    "bid": 1.07877,
    "ask": 1.07881
}
```

### `get_cross_price(symbol_code, time_frame)`

Latest price of a pair that isn't listed directly, derived from listed pairs (XAUVND = XAUUSD × USDVND, VNDUSD = 1 / USDVND). Every leg must be on your plan. High, low and volume are not available.

```python
xau_vnd = client.get_cross_price("XAUVND", "M1")
```

Example response payload:

```json
{
    "symbolCode": "XAUVND",
    "baseCurrency": "XAU",
    "quoteCurrency": "VND",
    "timeFrame": "M1",
    "bid": 106558131.0,
    "ask": 106647032.0,
    "openPrice": 106540000.0,
    "closePrice": 106600000.0,
    "openTime": "2026-11-21T09:12:00Z",
    "legs": [
        {"symbolCode": "XAUUSD", "from": "XAU", "to": "USD", "inverted": false, "bid": 4050.1, "ask": 4050.4, "openPrice": 4049.5, "closePrice": 4050.2, "openTime": "2026-11-21T09:12:00Z"},
        {"symbolCode": "USDVND", "from": "USD", "to": "VND", "inverted": false, "bid": 26310.0, "ask": 26330.0, "openPrice": 26309.0, "closePrice": 26320.0, "openTime": "2026-11-21T09:12:00Z"}
    ]
}
```

### `get_market_prices()`, `get_price_by_category(category)`, `get_24hr_stats()`

Snapshots for every symbol on your plan (or one category such as `"Forex"`), and rolling 24-hour stats.

```python
market = client.get_market_prices()          # {"data": [...], "totalCount": n}
forex = client.get_price_by_category("Forex")
stats = client.get_24hr_stats()
```

### `get_candles(symbol_code, time_frame)`

Example:

```python
candles = client.get_candles("BTCUSDT", "M5")
```

Example response payload:

```json
{
    "data": [
        {
            "symbolCode": "BTCUSDT",
            "openTime": "2026-05-21T09:10:00Z",
            "openPrice": 68620.3,
            "highPrice": 68690.1,
            "lowPrice": 68588.7,
            "closePrice": 68655.8,
            "volume": 128.42
        }
    ],
    "totalCount": 1
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
    "currentPage": 1,
    "pageSize": 20,
    "totalPages": 14,
    "totalCount": 280,
    "data": [
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

### `get_symbols(market_class=None)`

Example:

```python
symbols = client.get_symbols()
crypto = client.get_symbols(market_class="Crypto")
```

Example response payload:

```json
{
    "data": [
        {"symbolCode": "XAUUSD", "displayName": "Gold / US Dollar", "marketClass": "Commodity"}
    ],
    "totalCount": 1
}
```

### `get_cross_symbols(base_currency=None, quote_currency=None)`

Cross pairs `get_cross_price` can derive, with the listed symbols each one is built from. Listed symbols themselves are not included.

```python
crosses = client.get_cross_symbols(base_currency="XAU", quote_currency="VND")
```

Example response payload:

```json
{
    "data": [
        {"symbolCode": "XAUVND", "displayName": "XAU/VND", "baseCurrency": "XAU", "quoteCurrency": "VND", "legs": ["XAUUSD", "USDVND"]}
    ],
    "totalCount": 1
}
```

### `get_me()`

Plan code, request count/limit, usage percentage and WebSocket limits for your API key.

### `get_sma(symbol_code, time_frame, period=20)`

Example:

```python
sma = client.get_sma("EURUSD", "M15", period=50)
```

Example response payload:

```json
{
    "data": [
        {"openTime": "2026-05-21T09:00:00Z", "value": 1.08024}
    ],
    "totalCount": 1
}
```

### Other indicators

All take `(symbol_code, time_frame, ...)`; defaults match the API.

| Method | Extra params (default) |
|---|---|
| `get_ema` | `period=20` |
| `get_wma` | `period=20` |
| `get_rsi` | `period=14` |
| `get_macd` | `fast_period=12, slow_period=26, signal_period=9` |
| `get_bollinger_bands` | `period=20, multiplier=2.0` |
| `get_stochastic` | `k_period=14, d_period=3` |
| `get_atr` | `period=14` |
| `get_cci` | `period=20` |
| `get_williams_r` | `period=14` |
| `get_adx` | `period=14` |
| `get_fibonacci` | `lookback=100` |
| `get_support_resistance` | none |
| `get_sentiment` | none |

```python
macd = client.get_macd("XAUUSD", "H1")
bands = client.get_bollinger_bands("BTCUSD", "M15", multiplier=2.5)
```

### Volatility

| Method | Extra params (default) |
|---|---|
| `get_volatility(symbol_code, time_frame, period=14)` | `period` |
| `get_volatility_spikes(symbol_code, time_frame, period=14, spike_multiplier=2.0)` | `period`, `spike_multiplier` |
| `get_volatility_heatmap(symbol_code, time_frame)` | none |

### Market analysis

- `get_anomaly(symbol_code, time_frame)`
- `get_liquidity_zones(symbol_code, time_frame)`
- `get_manipulation_risk(symbol_code, time_frame)`
- `get_order_flow_imbalance(symbol_code, time_frame)`
- `get_stop_hunt_zones(symbol_code, time_frame)`
- `get_multi_timeframe(symbol_code)`: trend label per timeframe

### Insight

- `get_insight_next(symbol_code, time_frame)`: bias, bull/bear score, targets, signals
- `get_insight_trend(symbol_code, time_frame)`
- `get_insight_setup(symbol_code, time_frame)`
- `get_insight_confluence(symbol_code, time_frame)`
- `get_insight_score(symbol_code, time_frame)`: 0–100 score and label

```python
nxt = client.get_insight_next("XAUUSD", "H1")
print(nxt["bias"], nxt["targetUp"], nxt["targetDown"])
```

### `create_alert(symbol_code, time_frame, rule_type, threshold, cooldown_seconds=300, channels=None)`

Creates a new alert rule.

### `get_alerts(status=None)`

Returns alert rules, optionally filtered by status.

### `delete_alert(alert_id)`

Deletes an alert rule by id.

### `query_screener(time_frame, trend=None, min_rsi=None, max_volatility_pct=None, min_liquidity_score=None, sort_field="SignalScore", sort_direction="Desc", size=25)`

Queries symbols by screener filters.

### `get_strategy_signal(symbol_code, time_frame)`

Returns composite strategy signal payload.

### `create_watchlist(name, tags=None, notes=None)`

Creates a cloud watchlist.

### `get_watchlists()`

Returns watchlist collection.

### `add_watchlist_item(watchlist_id, symbol_code, order=0)`

Adds a symbol to a watchlist.

### `remove_watchlist_item(watchlist_id, symbol_code)`

Removes a symbol from a watchlist.

### `get_market_calendar(date=None, timezone="UTC")`

Returns sessions and high-impact market events.

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
    "openTime": "2026-05-21T09:10:00Z",
    "openPrice": 68620.3,
    "highPrice": 68690.1,
    "lowPrice": 68588.7,
    "closePrice": 68655.8,
    "volume": 128.42
}
```

### `stream_order_flow_imbalance(symbol_code, time_frame)`, `stream_multi_timeframe(symbol_code)`, `stream_market()`

Order flow imbalance updates, multi-timeframe trend updates, and full-market snapshots (each `stream_market` message is a list with one entry per symbol).

```python
async for snapshot in ws.stream_market():
    print(len(snapshot), "symbols")
```

## Error handling notes

- REST methods call `response.raise_for_status()`, so HTTP 4xx/5xx responses raise `httpx.HTTPStatusError`.
- WebSocket streams retry on connection errors using `reconnect_delay_seconds` (default `2.0`).
- Cancel the async task to stop streaming cleanly.

## Beta scope and compatibility

- REST coverage matches the .NET SDK: prices (single, market, category, 24h), candles, history, symbols, account (`get_me`), all indicators, volatility, anomaly, liquidity, manipulation risk, order flow, stop hunt, multi-timeframe, insight, alerts, screener, strategy signal, watchlists and market calendar.
- WebSocket coverage: price, candles, order flow imbalance, multi-timeframe and market.
- Not included: the MCP client (use any MCP client against the RealMarketAPI MCP server).
- This package is beta and may receive additive changes before stable `1.0`.

## Links

- RealMarketAPI homepage: [https://realmarketapi.com/](https://realmarketapi.com/)
