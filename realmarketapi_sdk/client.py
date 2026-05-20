from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import httpx


@dataclass
class RealMarketApiClient:
    api_key: str
    base_url: str = "https://api.realmarketapi.com"
    timeout_seconds: float = 20.0

    def __post_init__(self) -> None:
        self.base_url = self.base_url.rstrip("/")
        self._http = httpx.Client(timeout=self.timeout_seconds)

    def close(self) -> None:
        self._http.close()

    def get_price(self, symbol_code: str, time_frame: str) -> Dict[str, Any]:
        return self._get("/api/v1/price", {"symbolCode": symbol_code, "timeFrame": time_frame})

    def get_candles(self, symbol_code: str, time_frame: str) -> Dict[str, Any]:
        return self._get("/api/v1/candle", {"symbolCode": symbol_code, "timeFrame": time_frame})

    def get_history(
        self,
        symbol_code: str,
        start_time: str,
        end_time: str,
        page_number: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        return self._get(
            "/api/v1/history",
            {
                "symbolCode": symbol_code,
                "startTime": start_time,
                "endTime": end_time,
                "pageNumber": str(page_number),
                "pageSize": str(page_size),
            },
        )

    def get_symbols(self) -> Dict[str, Any]:
        return self._get("/api/v1/symbol", None)

    def get_sma(self, symbol_code: str, time_frame: str, period: int = 20) -> Dict[str, Any]:
        return self._get(
            "/api/v1/indicator/sma",
            {"symbolCode": symbol_code, "timeFrame": time_frame, "period": str(period)},
        )

    def _get(self, path: str, query: Optional[Dict[str, str]]) -> Dict[str, Any]:
        params: Dict[str, str] = {"apiKey": self.api_key}
        if query:
            params.update(query)

        url = f"{self.base_url}{path}?{urlencode(params)}"
        response = self._http.get(url)
        response.raise_for_status()
        return response.json()
