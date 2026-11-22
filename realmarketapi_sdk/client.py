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

    def get_cross_price(self, symbol_code: str, time_frame: str) -> Dict[str, Any]:
        """Latest price of a cross pair not listed directly, derived from listed pairs
        (e.g. "XAUVND" = XAUUSD x USDVND). Every leg must be on the key's plan. No high/low/volume."""
        return self._get("/api/v1/price/cross", {"symbolCode": symbol_code, "timeFrame": time_frame})

    def get_market_prices(self) -> Dict[str, Any]:
        """Latest price snapshot for every symbol on the key's plan."""
        return self._get("/api/v1/price/market", None)

    def get_price_by_category(self, category: str) -> Dict[str, Any]:
        """Latest price snapshot for every symbol in a category (e.g. "Forex", "Crypto")."""
        return self._get("/api/v1/price/category", {"category": category})

    def get_24hr_stats(self) -> Dict[str, Any]:
        """Rolling 24-hour open/high/low/volume/change for every symbol on the key's plan."""
        return self._get("/api/v1/price/24hr", None)

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

    def get_symbols(self, market_class: Optional[str] = None) -> Dict[str, Any]:
        query: Dict[str, str] = {}
        if market_class:
            query["marketClass"] = market_class
        return self._get("/api/v1/symbol", query)

    def get_cross_symbols(
        self, base_currency: Optional[str] = None, quote_currency: Optional[str] = None
    ) -> Dict[str, Any]:
        """Cross pairs get_cross_price can derive, optionally filtered by base and/or quote currency."""
        query: Dict[str, str] = {}
        if base_currency:
            query["baseCurrency"] = base_currency
        if quote_currency:
            query["quoteCurrency"] = quote_currency
        return self._get("/api/v1/symbol/cross", query)

    def get_me(self) -> Dict[str, Any]:
        """Plan, quota usage and limits for the API key."""
        return self._get("/api/v1/me", None)

    def get_sma(self, symbol_code: str, time_frame: str, period: int = 20) -> Dict[str, Any]:
        return self._get(
            "/api/v1/indicator/sma",
            {"symbolCode": symbol_code, "timeFrame": time_frame, "period": str(period)},
        )

    def get_ema(self, symbol_code: str, time_frame: str, period: int = 20) -> Dict[str, Any]:
        return self._get(
            "/api/v1/indicator/ema",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
                "period": str(period),
            },
        )

    def get_wma(self, symbol_code: str, time_frame: str, period: int = 20) -> Dict[str, Any]:
        return self._get(
            "/api/v1/indicator/wma",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
                "period": str(period),
            },
        )

    def get_rsi(self, symbol_code: str, time_frame: str, period: int = 14) -> Dict[str, Any]:
        return self._get(
            "/api/v1/indicator/rsi",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
                "period": str(period),
            },
        )

    def get_macd(self, symbol_code: str, time_frame: str, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> Dict[str, Any]:
        return self._get(
            "/api/v1/indicator/macd",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
                "fastPeriod": str(fast_period),
                "slowPeriod": str(slow_period),
                "signalPeriod": str(signal_period),
            },
        )

    def get_support_resistance(self, symbol_code: str, time_frame: str) -> Dict[str, Any]:
        return self._get(
            "/api/v1/indicator/support-resistance",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
            },
        )

    def get_fibonacci(self, symbol_code: str, time_frame: str, lookback: int = 100) -> Dict[str, Any]:
        return self._get(
            "/api/v1/indicator/fibonacci",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
                "lookback": str(lookback),
            },
        )

    def get_bollinger_bands(self, symbol_code: str, time_frame: str, period: int = 20, multiplier: float = 2.0) -> Dict[str, Any]:
        return self._get(
            "/api/v1/indicator/bollinger-bands",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
                "period": str(period),
                "multiplier": _num(multiplier),
            },
        )

    def get_stochastic(self, symbol_code: str, time_frame: str, k_period: int = 14, d_period: int = 3) -> Dict[str, Any]:
        return self._get(
            "/api/v1/indicator/stochastic",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
                "kPeriod": str(k_period),
                "dPeriod": str(d_period),
            },
        )

    def get_atr(self, symbol_code: str, time_frame: str, period: int = 14) -> Dict[str, Any]:
        return self._get(
            "/api/v1/indicator/atr",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
                "period": str(period),
            },
        )

    def get_cci(self, symbol_code: str, time_frame: str, period: int = 20) -> Dict[str, Any]:
        return self._get(
            "/api/v1/indicator/cci",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
                "period": str(period),
            },
        )

    def get_williams_r(self, symbol_code: str, time_frame: str, period: int = 14) -> Dict[str, Any]:
        return self._get(
            "/api/v1/indicator/williams-r",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
                "period": str(period),
            },
        )

    def get_adx(self, symbol_code: str, time_frame: str, period: int = 14) -> Dict[str, Any]:
        return self._get(
            "/api/v1/indicator/adx",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
                "period": str(period),
            },
        )

    def get_sentiment(self, symbol_code: str, time_frame: str) -> Dict[str, Any]:
        return self._get(
            "/api/v1/indicator/sentiment",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
            },
        )

    def get_volatility(self, symbol_code: str, time_frame: str, period: int = 14) -> Dict[str, Any]:
        return self._get(
            "/api/v1/volatility",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
                "period": str(period),
            },
        )

    def get_volatility_spikes(self, symbol_code: str, time_frame: str, period: int = 14, spike_multiplier: float = 2.0) -> Dict[str, Any]:
        return self._get(
            "/api/v1/volatility/spikes",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
                "period": str(period),
                "spikeMultiplier": _num(spike_multiplier),
            },
        )

    def get_volatility_heatmap(self, symbol_code: str, time_frame: str) -> Dict[str, Any]:
        return self._get(
            "/api/v1/volatility/heatmap",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
            },
        )

    def get_anomaly(self, symbol_code: str, time_frame: str) -> Dict[str, Any]:
        return self._get(
            "/api/v1/anomaly",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
            },
        )

    def get_liquidity_zones(self, symbol_code: str, time_frame: str) -> Dict[str, Any]:
        return self._get(
            "/api/v1/liquidity/zones",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
            },
        )

    def get_manipulation_risk(self, symbol_code: str, time_frame: str) -> Dict[str, Any]:
        return self._get(
            "/api/v1/manipulation-risk",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
            },
        )

    def get_order_flow_imbalance(self, symbol_code: str, time_frame: str) -> Dict[str, Any]:
        return self._get(
            "/api/v1/orderflow/imbalance",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
            },
        )

    def get_stop_hunt_zones(self, symbol_code: str, time_frame: str) -> Dict[str, Any]:
        return self._get(
            "/api/v1/stop-hunt/zones",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
            },
        )

    def get_multi_timeframe(self, symbol_code: str) -> Dict[str, Any]:
        """Trend label per timeframe for one symbol."""
        return self._get("/api/v1/multi-timeframe", {"symbolCode": symbol_code})

    def get_insight_next(self, symbol_code: str, time_frame: str) -> Dict[str, Any]:
        return self._get(
            "/api/v1/insight/next",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
            },
        )

    def get_insight_trend(self, symbol_code: str, time_frame: str) -> Dict[str, Any]:
        return self._get(
            "/api/v1/insight/trend",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
            },
        )

    def get_insight_setup(self, symbol_code: str, time_frame: str) -> Dict[str, Any]:
        return self._get(
            "/api/v1/insight/setup",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
            },
        )

    def get_insight_confluence(self, symbol_code: str, time_frame: str) -> Dict[str, Any]:
        return self._get(
            "/api/v1/insight/confluence",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
            },
        )

    def get_insight_score(self, symbol_code: str, time_frame: str) -> Dict[str, Any]:
        return self._get(
            "/api/v1/insight/score",
            {
                "symbolCode": symbol_code,
                "timeFrame": time_frame,
            },
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


def _num(value: float) -> str:
    """Format a number for the query string without a trailing ".0" (2.0 -> "2", 2.5 -> "2.5")."""
    return str(int(value)) if float(value).is_integer() else repr(float(value))
