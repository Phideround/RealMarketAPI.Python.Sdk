from __future__ import annotations

import asyncio
import json
import unittest
from typing import Any, AsyncIterator, Callable, Dict, Tuple
from urllib.parse import parse_qsl, urlsplit

from realmarketapi_sdk import RealMarketApiWebSocket

try:
    from websockets.asyncio.server import serve  # websockets >= 13
except ImportError:  # pragma: no cover
    serve = None

Open = Callable[[RealMarketApiWebSocket], AsyncIterator[Any]]

CASES = [
    ("stream_price", lambda ws: ws.stream_price("XAUUSD", "M1"), "/price", {"symbolCode": "XAUUSD", "timeFrame": "M1"}, {"closePrice": 1}),
    ("stream_candles", lambda ws: ws.stream_candles("XAUUSD", "M5"), "/candles", {"symbolCode": "XAUUSD", "timeFrame": "M5"}, {"openPrice": 1}),
    (
        "stream_order_flow_imbalance",
        lambda ws: ws.stream_order_flow_imbalance("XAUUSD", "H1"),
        "/orderflow/imbalance",
        {"symbolCode": "XAUUSD", "timeFrame": "H1"},
        {"currentImbalance": "Bullish"},
    ),
    (
        "stream_multi_timeframe",
        lambda ws: ws.stream_multi_timeframe("BTCUSD"),
        "/multi-timeframe",
        {"symbolCode": "BTCUSD"},
        {"timeframes": {"H1": "Bullish"}},
    ),
    ("stream_market", lambda ws: ws.stream_market(), "/market", {}, [{"symbolCode": "XAUUSD", "closePrice": 1}]),
]


async def run_stream(open_stream: Open, payload: Any) -> Tuple[str, Dict[str, str], Any]:
    seen: Dict[str, str] = {}

    async def handler(connection: Any) -> None:
        seen["path"] = connection.request.path
        await connection.send(json.dumps(payload))
        await connection.wait_closed()

    async with serve(handler, "127.0.0.1", 0) as server:
        port = next(iter(server.sockets)).getsockname()[1]
        ws = RealMarketApiWebSocket(api_key="key-123", base_url=f"http://127.0.0.1:{port}")
        stream = open_stream(ws)
        try:
            message = await asyncio.wait_for(stream.__anext__(), timeout=5)
        finally:
            await stream.aclose()

    parts = urlsplit(seen["path"])
    return parts.path, dict(parse_qsl(parts.query)), message


@unittest.skipIf(serve is None, "needs websockets >= 13 for the test server")
class WebSocketTests(unittest.TestCase):
    def test_streams(self) -> None:
        for name, open_stream, path, query, payload in CASES:
            with self.subTest(name):
                got_path, params, message = asyncio.run(run_stream(open_stream, payload))
                self.assertEqual(got_path, path)
                self.assertEqual(params.pop("apiKey"), "key-123")
                self.assertEqual(params, query)
                self.assertEqual(message, payload)


if __name__ == "__main__":
    unittest.main()
