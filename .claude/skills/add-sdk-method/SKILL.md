---
name: add-sdk-method
description: Add a method to the RealMarketAPI Python SDK for a backend endpoint. Use when the user wants the Python SDK to support a new or changed RealMarketAPI endpoint.
---

# Add an SDK method (Python)

## 1. Get the contract
Prefer the .NET SDK as the reference (`../RealMarketAPI.Sdk/Clients/I<Area>Client.cs`), since it documents the route, params and defaults. Fall back to the backend handler in `../RealTimeMarketAPI/sources/RealTimeMarketAPI.Core/Modules/`. Mirror the JS SDK method name in snake_case when it exists.

## 2. Method — `realmarketapi_sdk/client.py`
Add it next to related methods, before the private helpers:

```python
def get_volatility(self, symbol_code: str, time_frame: str, period: int = 14) -> Dict[str, Any]:
    return self._get(
        "/api/v1/volatility",
        {"symbolCode": symbol_code, "timeFrame": time_frame, "period": str(period)},
    )
```

- POST: `self._post(path, payload)` with camelCase payload keys; DELETE: `self._delete(path)`.
- Optional params: build the dict and only add keys that are set (see `get_market_calendar`).
- Keep it 3.9-compatible: `Optional[str]`, not `str | None`.
- `apiKey` is added by the helpers; never pass it yourself.

## 3. Finish
- README: add an example.
- If preparing a release, bump `version` in `pyproject.toml` keeping the `bN` suffix.
- `python -m build` must pass (or at least `python -c "import realmarketapi_sdk"` if `build` isn't installed).
