from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import Any, AsyncIterator, Dict
from urllib.parse import urlencode, urlparse

import websockets


@dataclass
class RealMarketApiWebSocket:
    api_key: str
    base_url: str = "https://api.realmarketapi.com"
    reconnect_delay_seconds: float = 2.0

    async def stream_price(self, symbol_code: str, time_frame: str) -> AsyncIterator[Dict[str, Any]]:
        async for item in self._stream("price", {"symbolCode": symbol_code, "timeFrame": time_frame}):
            yield item

    async def stream_candles(self, symbol_code: str, time_frame: str) -> AsyncIterator[Dict[str, Any]]:
        async for item in self._stream("candles", {"symbolCode": symbol_code, "timeFrame": time_frame}):
            yield item

    async def _stream(self, endpoint: str, params: Dict[str, str]) -> AsyncIterator[Dict[str, Any]]:
        closed_by_user = False

        while not closed_by_user:
            url = self._to_ws_url(endpoint, params)
            try:
                async with websockets.connect(url) as socket:
                    while True:
                        raw = await socket.recv()
                        yield json.loads(raw)
            except asyncio.CancelledError:
                closed_by_user = True
            except Exception:
                await asyncio.sleep(self.reconnect_delay_seconds)

    def _to_ws_url(self, endpoint: str, params: Dict[str, str]) -> str:
        parsed = urlparse(self.base_url.rstrip("/"))
        scheme = "wss" if parsed.scheme == "https" else "ws"
        query = urlencode({"apiKey": self.api_key, **params})
        return f"{scheme}://{parsed.netloc}/{endpoint}?{query}"
