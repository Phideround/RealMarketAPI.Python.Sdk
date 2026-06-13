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

    def create_alert(
        self,
        symbol_code: str,
        time_frame: str,
        rule_type: str,
        threshold: float,
        cooldown_seconds: int = 300,
        channels: Optional[list[str]] = None,
    ) -> Dict[str, Any]:
        return self._post(
            "/api/v1/alerts",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
                "ruleType": rule_type,
                "threshold": threshold,
                "cooldownSeconds": cooldown_seconds,
                "channels": channels or [],
            },
        )

    def get_alerts(self, status: Optional[str] = None) -> Dict[str, Any]:
        query: Dict[str, str] = {}
        if status:
            query["status"] = status
        return self._get("/api/v1/alerts", query)

    def delete_alert(self, alert_id: str) -> Dict[str, Any]:
        return self._delete(f"/api/v1/alerts/{alert_id}")

    def query_screener(
        self,
        time_frame: str,
        trend: Optional[str] = None,
        min_rsi: Optional[float] = None,
        max_volatility_pct: Optional[float] = None,
        min_liquidity_score: Optional[float] = None,
        sort_field: str = "SignalScore",
        sort_direction: str = "Desc",
        size: int = 25,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "timeFrame": time_frame,
            "sortField": sort_field,
            "sortDirection": sort_direction,
            "size": size,
        }
        if trend is not None:
            payload["trend"] = trend
        if min_rsi is not None:
            payload["minRsi"] = min_rsi
        if max_volatility_pct is not None:
            payload["maxVolatilityPct"] = max_volatility_pct
        if min_liquidity_score is not None:
            payload["minLiquidityScore"] = min_liquidity_score
        return self._post("/api/v1/screener/query", payload)

    def get_strategy_signal(self, symbol_code: str, time_frame: str) -> Dict[str, Any]:
        return self._get(
            "/api/v1/signals/strategy",
            {"symbolCode": symbol_code, "timeFrame": time_frame},
        )

    def create_watchlist(
        self, name: str, tags: Optional[list[str]] = None, notes: Optional[str] = None
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"name": name, "tags": tags or []}
        if notes is not None:
            payload["notes"] = notes
        return self._post("/api/v1/watchlists", payload)

    def get_watchlists(self) -> Dict[str, Any]:
        return self._get("/api/v1/watchlists", None)

    def add_watchlist_item(self, watchlist_id: str, symbol_code: str, order: int = 0) -> Dict[str, Any]:
        return self._post(
            f"/api/v1/watchlists/{watchlist_id}/items",
            {"symbolCode": symbol_code, "order": order},
        )

    def remove_watchlist_item(self, watchlist_id: str, symbol_code: str) -> Dict[str, Any]:
        return self._delete(f"/api/v1/watchlists/{watchlist_id}/items/{symbol_code}")

    def get_market_calendar(self, date: Optional[str] = None, timezone: str = "UTC") -> Dict[str, Any]:
        query: Dict[str, str] = {"timezone": timezone}
        if date:
            query["date"] = date
        return self._get("/api/v1/market-calendar", query)

    def _get(self, path: str, query: Optional[Dict[str, str]]) -> Dict[str, Any]:
        params: Dict[str, str] = {"apiKey": self.api_key}
        if query:
            params.update(query)

        url = f"{self.base_url}{path}?{urlencode(params)}"
        response = self._http.get(url)
        response.raise_for_status()
        return response.json()

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        params: Dict[str, str] = {"apiKey": self.api_key}
        url = f"{self.base_url}{path}?{urlencode(params)}"
        response = self._http.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def _delete(self, path: str) -> Dict[str, Any]:
        params: Dict[str, str] = {"apiKey": self.api_key}
        url = f"{self.base_url}{path}?{urlencode(params)}"
        response = self._http.delete(url)
        response.raise_for_status()
        return response.json()
