# RealMarketAPI Python SDK (beta)

Python SDK for RealMarketAPI, published to PyPI as `realmarketapi-python-sdk-beta`. Package `realmarketapi_sdk`, Python 3.9+, dependencies `httpx` and `websockets`, built with setuptools (`pyproject.toml`).

## Commands

```bash
python -m pip install -e .
python -m build                 # sdist + wheel in dist/
python -m twine check dist/*    # if twine is installed
python -m unittest discover -s tests -v
```

No linter. Tests use stdlib `unittest` (no extra dev dependency): REST through `httpx.MockTransport` swapped into `client._http`, streams against a local `websockets` server. Add a row to the case table in `tests/test_client.py` or `tests/test_websocket.py` for each new method.

## Layout

| File | What |
|---|---|
| `realmarketapi_sdk/client.py` | `RealMarketApiClient` dataclass (`api_key`, `base_url`, `timeout_seconds`), sync `httpx.Client`. One method per endpoint plus `_get/_post/_delete`, which add `apiKey` to the query and call `raise_for_status()`. Call `close()` when done. |
| `realmarketapi_sdk/websocket.py` | `RealMarketApiWebSocket`: async generators `stream_price`, `stream_candles`, `stream_order_flow_imbalance`, `stream_multi_timeframe`, `stream_market` with reconnect. |
| `realmarketapi_sdk/__init__.py` | Exports both classes via `__all__`. |

Methods return the parsed JSON as `Dict[str, Any]`; there are no model classes. Coverage matches the JS SDK and the .NET SDK, except the .NET MCP client.

## Conventions

- Python 3.9 compatible typing: `Dict`, `Optional`, `List` from `typing` (no `X | None`), with `from __future__ import annotations` at the top.
- Method and argument names are snake_case (`get_price(symbol_code, time_frame)`); query keys stay camelCase as the API expects (`"symbolCode"`). Query values are strings (`str(period)`).
- Paths start with `/api/v1/`.

## Releasing

Version in `pyproject.toml` must contain `b` (e.g. `0.1.0b3`). Pushing the tag `py-sdk-v<version>` runs `.github/workflows/publish-pypi-beta.yml`. Never tag or push without the user asking. Skill: `add-sdk-method`.
