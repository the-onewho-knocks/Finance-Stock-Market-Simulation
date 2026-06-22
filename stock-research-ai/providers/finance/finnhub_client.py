import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from core.cache import cache_get, cache_set
from core.config import settings
from core.exceptions import ProviderError
from loguru import logger

BASE = "https://finnhub.io/api/v1"

class FinhubClient:
    def __init__(self):
        self._key = settings.finnhub_api_key

    async def get_company_news(self, symbol: str, from_date: str, to_date: str) -> list[dict]:
        cache_key = f"news:{symbol.upper()}:{from_date}:{to_date}"
        cached = await cache_get("finnhub", cache_key)
        if cached:
            return cached
        url = f"{BASE}/company-news"
        params = {"symbol": symbol, "from": from_date, "to": to_date, "token": self._key}
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, params=params)
        if resp.status_code != 200:
            raise ProviderError("finnhub error", f"news failed: {resp.text}")
        data = resp.json()
        await cache_set("finnhub", cache_key, data, ttl=300)
        return data
    
    async def get_quote(self, symbol: str) -> dict:
        cached = await cache_get("finnhub", f"quote:{symbol.upper()}")
        if cached:
            return cached
        url = f"{BASE}/quote"
        params = {"symbol": symbol, "token": self._key}
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, params=params)
        if resp.status_code != 200:
            raise ProviderError("finnhub error", f"quote failed: {resp.text}")
        data = resp.json()
        await cache_set("finnhub", f"quote:{symbol.upper()}", data, ttl=60)
        return data
    
    
    async def get_company_profile(self, symbol: str) -> dict:
        cached = await cache_get("finnhub", f"profile:{symbol.upper()}")
        if cached:
            return cached
        url = f"{BASE}/stock/profile2"
        params = {"symbol": symbol, "token": self._key}
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, params=params)
        if resp.status_code != 200:
            raise ProviderError("finnhub", f"profile failed: {resp.text}")
        data = resp.json()
        await cache_set("finnhub", f"profile:{symbol.upper()}", data, ttl=3600)
        return data