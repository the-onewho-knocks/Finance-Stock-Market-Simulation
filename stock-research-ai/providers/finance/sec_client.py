import json

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from core.exceptions import ProviderError

BASE = "https://efts.sec.gov/LATEST/search-index"


class SECClient:
    HEADERS = {
        "User-Agent": "StockResearchAI/1.0 (drj2905@gmail.com)",
        "Accept-Encoding": "gzip, deflate",
        "Host": "efts.sec.gov",
    }

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(min=1, max=8),
    )
    async def search_filings(
        self,
        query: str,
        form_type: str = "10-K",
        hits: int = 5,
    ) -> list[dict]:
        params = {
            "q": query,
            "forms": form_type,
            "size": hits,
        }

        async with httpx.AsyncClient(timeout=20, headers=self.HEADERS) as c:
            r = await c.get(BASE, params=params)

        if r.status_code != 200:
            raise ProviderError("sec", f"status {r.status_code}: {r.text[:200]}")

        content_type = r.headers.get("content-type", "")
        if "json" not in content_type:
            raise ProviderError(
                "sec",
                f"Expected JSON, got {content_type}: {r.text[:200]}",
            )

        try:
            data = r.json()
        except json.JSONDecodeError:
            raise ProviderError(
                "sec",
                f"Non-JSON response: {r.text[:200]}",
            )

        hits_list = data.get("hits", {}).get("hits", [])
        return [h.get("_source", {}) for h in hits_list[:hits]]

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(min=1, max=8),
    )
    async def get_filing_document(self, url: str) -> str:
        async with httpx.AsyncClient(timeout=30, headers=self.HEADERS) as c:
            r = await c.get(url)

        if r.status_code != 200:
            raise ProviderError("sec", f"doc fetch failed: {r.status_code}")

        return r.text