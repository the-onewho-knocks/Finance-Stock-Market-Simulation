import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from core.config import settings
from core.exceptions import ProviderError
from core.cache import cache_get, cache_set

BASE = "https://api.polygon.io/v2"

class PolygonClient:
    def __init__(self):
        self._key = settings.polygon_api_key

    async def get_aggregates(
    self, symbol: str, from_date: str,
    to_date: str,
    multiplier: int = 1, timespan: str = "day"
    ):
        cache_key = f"agg:{symbol.upper()}:{from_date}:{to_date}:{multiplier}:{timespan}"
        cached = await cache_get("polygon", cache_key)
        if cached:
            return cached
        url = f"{BASE}/aggs/ticker/{symbol}/range/{multiplier}/{timespan}/{from_date}/{to_date}"
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(url, params={"apiKey": self._key, "adjusted": "true", "sort": "asc"})
        if r.status_code != 200:
            raise ProviderError("polygon error", f"aggregates failed: {r.text}")
        data = r.json()
        await cache_set("polygon", cache_key, data, ttl=3600)
        return data
    
    async def get_ticker_details(self, symbol: str) -> dict:
        cached = await cache_get("polygon", f"details:{symbol.upper()}")
        if cached:
            return cached
        url = f"https://api.polygon.io/v3/reference/tickers/{symbol}"
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(url, params={"apiKey": self._key})
        if r.status_code != 200:
            raise ProviderError("polygon error", f"ticker details failed: {r.text}")
        data = r.json()
        await cache_set("polygon", f"details:{symbol.upper()}", data, ttl=3600)
        return data