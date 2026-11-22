from __future__ import annotations

import json
import unittest
from typing import Any, Callable, Dict, List, Tuple

import httpx

from realmarketapi_sdk import RealMarketApiClient

BASE = "https://api.test.local"


def make_client(body: Any = None, status: int = 200) -> Tuple[RealMarketApiClient, List[httpx.Request]]:
    """Client whose HTTP calls are captured and answered with `body`."""
    requests: List[httpx.Request] = []
    payload = {"data": [], "totalCount": 0} if body is None else body

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(status, json=payload)

    client = RealMarketApiClient(api_key="key-123", base_url=f"{BASE}/")
    client._http.close()
    client._http = httpx.Client(transport=httpx.MockTransport(handler))
    return client, requests


Case = Tuple[str, Callable[[RealMarketApiClient], Any], str, Dict[str, str]]

S = {"symbolCode": "XAUUSD", "timeFrame": "H1"}

GET_CASES: List[Case] = [
    ("get_price", lambda c: c.get_price("XAUUSD", "M1"), "/api/v1/price", {"symbolCode": "XAUUSD", "timeFrame": "M1"}),
    (
        "get_cross_price",
        lambda c: c.get_cross_price("XAUVND", "M1"),
        "/api/v1/price/cross",
        {"symbolCode": "XAUVND", "timeFrame": "M1"},
    ),
    ("get_market_prices", lambda c: c.get_market_prices(), "/api/v1/price/market", {}),
    ("get_price_by_category", lambda c: c.get_price_by_category("Forex"), "/api/v1/price/category", {"category": "Forex"}),
    ("get_24hr_stats", lambda c: c.get_24hr_stats(), "/api/v1/price/24hr", {}),
    ("get_candles", lambda c: c.get_candles("XAUUSD", "H1"), "/api/v1/candle", S),
    (
        "get_history",
        lambda c: c.get_history("XAUUSD", "2026-01-01T00:00:00Z", "2026-01-02T00:00:00Z"),
        "/api/v1/history",
        {
            "symbolCode": "XAUUSD",
            "startTime": "2026-01-01T00:00:00Z",
            "endTime": "2026-01-02T00:00:00Z",
            "pageNumber": "1",
            "pageSize": "20",
        },
    ),
    ("get_symbols", lambda c: c.get_symbols(), "/api/v1/symbol", {}),
    ("get_symbols(market_class)", lambda c: c.get_symbols("Crypto"), "/api/v1/symbol", {"marketClass": "Crypto"}),
    ("get_cross_symbols", lambda c: c.get_cross_symbols(), "/api/v1/symbol/cross", {}),
    (
        "get_cross_symbols(base_currency, quote_currency)",
        lambda c: c.get_cross_symbols("XAU", "VND"),
        "/api/v1/symbol/cross",
        {"baseCurrency": "XAU", "quoteCurrency": "VND"},
    ),
    ("get_me", lambda c: c.get_me(), "/api/v1/me", {}),
    ("get_sma", lambda c: c.get_sma("XAUUSD", "H1"), "/api/v1/indicator/sma", {**S, "period": "20"}),
    ("get_ema", lambda c: c.get_ema("XAUUSD", "H1", 50), "/api/v1/indicator/ema", {**S, "period": "50"}),
    ("get_wma", lambda c: c.get_wma("XAUUSD", "H1"), "/api/v1/indicator/wma", {**S, "period": "20"}),
    ("get_rsi", lambda c: c.get_rsi("XAUUSD", "H1"), "/api/v1/indicator/rsi", {**S, "period": "14"}),
    (
        "get_macd",
        lambda c: c.get_macd("XAUUSD", "H1"),
        "/api/v1/indicator/macd",
        {**S, "fastPeriod": "12", "slowPeriod": "26", "signalPeriod": "9"},
    ),
    ("get_support_resistance", lambda c: c.get_support_resistance("XAUUSD", "H1"), "/api/v1/indicator/support-resistance", S),
    ("get_fibonacci", lambda c: c.get_fibonacci("XAUUSD", "H1"), "/api/v1/indicator/fibonacci", {**S, "lookback": "100"}),
    (
        "get_bollinger_bands",
        lambda c: c.get_bollinger_bands("XAUUSD", "H1"),
        "/api/v1/indicator/bollinger-bands",
        {**S, "period": "20", "multiplier": "2"},
    ),
    (
        "get_bollinger_bands(2.5)",
        lambda c: c.get_bollinger_bands("XAUUSD", "H1", multiplier=2.5),
        "/api/v1/indicator/bollinger-bands",
        {**S, "period": "20", "multiplier": "2.5"},
    ),
    ("get_stochastic", lambda c: c.get_stochastic("XAUUSD", "H1"), "/api/v1/indicator/stochastic", {**S, "kPeriod": "14", "dPeriod": "3"}),
    ("get_atr", lambda c: c.get_atr("XAUUSD", "H1"), "/api/v1/indicator/atr", {**S, "period": "14"}),
    ("get_cci", lambda c: c.get_cci("XAUUSD", "H1"), "/api/v1/indicator/cci", {**S, "period": "20"}),
    ("get_williams_r", lambda c: c.get_williams_r("XAUUSD", "H1"), "/api/v1/indicator/williams-r", {**S, "period": "14"}),
    ("get_adx", lambda c: c.get_adx("XAUUSD", "H1"), "/api/v1/indicator/adx", {**S, "period": "14"}),
    ("get_sentiment", lambda c: c.get_sentiment("XAUUSD", "H1"), "/api/v1/indicator/sentiment", S),
    ("get_volatility", lambda c: c.get_volatility("XAUUSD", "H1"), "/api/v1/volatility", {**S, "period": "14"}),
    (
        "get_volatility_spikes",
        lambda c: c.get_volatility_spikes("XAUUSD", "H1"),
        "/api/v1/volatility/spikes",
        {**S, "period": "14", "spikeMultiplier": "2"},
    ),
    ("get_volatility_heatmap", lambda c: c.get_volatility_heatmap("XAUUSD", "H1"), "/api/v1/volatility/heatmap", S),
    ("get_anomaly", lambda c: c.get_anomaly("XAUUSD", "H1"), "/api/v1/anomaly", S),
    ("get_liquidity_zones", lambda c: c.get_liquidity_zones("XAUUSD", "H1"), "/api/v1/liquidity/zones", S),
    ("get_manipulation_risk", lambda c: c.get_manipulation_risk("XAUUSD", "H1"), "/api/v1/manipulation-risk", S),
    ("get_order_flow_imbalance", lambda c: c.get_order_flow_imbalance("XAUUSD", "H1"), "/api/v1/orderflow/imbalance", S),
    ("get_stop_hunt_zones", lambda c: c.get_stop_hunt_zones("XAUUSD", "H1"), "/api/v1/stop-hunt/zones", S),
    ("get_multi_timeframe", lambda c: c.get_multi_timeframe("XAUUSD"), "/api/v1/multi-timeframe", {"symbolCode": "XAUUSD"}),
    ("get_insight_next", lambda c: c.get_insight_next("XAUUSD", "H1"), "/api/v1/insight/next", S),
    ("get_insight_trend", lambda c: c.get_insight_trend("XAUUSD", "H1"), "/api/v1/insight/trend", S),
    ("get_insight_setup", lambda c: c.get_insight_setup("XAUUSD", "H1"), "/api/v1/insight/setup", S),
    ("get_insight_confluence", lambda c: c.get_insight_confluence("XAUUSD", "H1"), "/api/v1/insight/confluence", S),
    ("get_insight_score", lambda c: c.get_insight_score("XAUUSD", "H1"), "/api/v1/insight/score", S),
    ("get_alerts", lambda c: c.get_alerts("Active"), "/api/v1/alerts", {"status": "Active"}),
    ("get_strategy_signal", lambda c: c.get_strategy_signal("XAUUSD", "H1"), "/api/v1/signals/strategy", S),
    ("get_watchlists", lambda c: c.get_watchlists(), "/api/v1/watchlists", {}),
    (
        "get_market_calendar",
        lambda c: c.get_market_calendar("2026-11-21"),
        "/api/v1/market-calendar",
        {"timezone": "UTC", "date": "2026-11-21"},
    ),
]


class GetEndpointTests(unittest.TestCase):
    def test_routes_and_query(self) -> None:
        for name, invoke, path, query in GET_CASES:
            with self.subTest(name):
                client, requests = make_client()
                invoke(client)
                client.close()

                self.assertEqual(len(requests), 1)
                request = requests[0]
                self.assertEqual(request.method, "GET")
                self.assertEqual(f"{request.url.scheme}://{request.url.host}", BASE)
                self.assertEqual(request.url.path, path)

                params = dict(request.url.params)
                self.assertEqual(params.pop("apiKey"), "key-123")
                self.assertEqual(params, query)


class BehaviourTests(unittest.TestCase):
    def test_returns_parsed_json(self) -> None:
        body = {"symbolCode": "XAUUSD", "calculatedAt": "2026-11-21T00:00:00Z", "timeframes": {"H1": "Bullish"}}
        client, _ = make_client(body)
        self.assertEqual(client.get_multi_timeframe("XAUUSD"), body)

    def test_post_sends_json_body(self) -> None:
        client, requests = make_client({"alertId": "a1"})
        client.create_alert("XAUUSD", "M5", "PriceAbove", 2500)

        request = requests[0]
        self.assertEqual(request.method, "POST")
        self.assertEqual(request.url.path, "/api/v1/alerts")
        self.assertEqual(request.url.params["apiKey"], "key-123")
        self.assertEqual(
            json.loads(request.content),
            {
                "symbolCode": "XAUUSD",
                "timeFrame": "M5",
                "ruleType": "PriceAbove",
                "threshold": 2500,
                "cooldownSeconds": 300,
                "channels": [],
            },
        )

    def test_error_status_raises(self) -> None:
        client, _ = make_client({"errors": [{"errorCode": "ERR_0005_INVALID_API_KEY"}]}, status=401)
        with self.assertRaises(httpx.HTTPStatusError) as ctx:
            client.get_insight_score("XAUUSD", "H1")
        self.assertEqual(ctx.exception.response.status_code, 401)
        self.assertIn("ERR_0005_INVALID_API_KEY", ctx.exception.response.text)


if __name__ == "__main__":
    unittest.main()
