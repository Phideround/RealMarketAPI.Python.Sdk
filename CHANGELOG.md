# Changelog

All notable changes to `realmarketapi-python-sdk-beta` are listed here.

## 0.1.0b3 (2026-11-22)

REST and WebSocket coverage now matches the .NET SDK (`RealMarketAPI.Sdk`), except the MCP client.

### Added
- Prices: `get_market_prices()`, `get_price_by_category(category)`, `get_24hr_stats()`.
- Cross rates: `get_cross_price(symbol_code, time_frame)` (`GET /api/v1/price/cross`) and `get_cross_symbols(base_currency=None, quote_currency=None)` (`GET /api/v1/symbol/cross`) for pairs derived from listed ones, e.g. XAUVND = XAUUSD x USDVND.
- Account: `get_me()`.
- Indicators: `get_ema`, `get_wma`, `get_rsi`, `get_macd`, `get_bollinger_bands`, `get_stochastic`, `get_atr`, `get_cci`, `get_williams_r`, `get_adx`, `get_fibonacci`, `get_support_resistance`, `get_sentiment`.
- Volatility: `get_volatility`, `get_volatility_spikes`, `get_volatility_heatmap`.
- Market analysis: `get_anomaly`, `get_liquidity_zones`, `get_manipulation_risk`, `get_order_flow_imbalance`, `get_stop_hunt_zones`, `get_multi_timeframe`.
- Insight: `get_insight_next`, `get_insight_trend`, `get_insight_setup`, `get_insight_confluence`, `get_insight_score`.
- `get_symbols(market_class=None)` accepts an optional market class filter.
- WebSocket: `stream_order_flow_imbalance`, `stream_multi_timeframe`, `stream_market`.
- Test suite (`python -m unittest discover -s tests`).

### Fixed
- README example payloads now show the real response shapes (`data` / `totalCount`, `currentPage` for history, `bid` / `ask` on prices, `displayName` / `marketClass` on symbols).

## 0.1.0b2

- Price, candle, history, symbol, SMA, alerts, screener, strategy signal, watchlists and market calendar; price and candle WebSocket streams.
