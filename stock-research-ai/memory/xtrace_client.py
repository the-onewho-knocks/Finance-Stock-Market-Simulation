from typing import Any
from uuid import uuid4

import httpx
from loguru import logger

from core.config import settings
from memory.schemas import MemoryRecord, MemorySearchResult, MemoryStoreResult


class XTraceMemoryProvider:
    
    provider_name = "xtrace"

    def __init__(self):
        self.api_key = settings.xtrace_api_key
        self.base_url = getattr(settings, "xtrace_base_url", "")

    @property
    def available(self) -> bool:
        return bool(self.api_key and self.base_url)

    def _header(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    '''
    This class is a wrapper around the XTrace memory API. Its job is:
        Check if XTrace is configured.
        Send a search request to XTrace.
        Convert the response into your application's MemoryRecord objects.
        Never crash the research workflow if XTrace fails.
    '''
    async def search(
        self,
        query: str,
        *,
        user_id: str | None = None,
        symbol: str | None = None,
        limit: int = 5,
    ) -> MemorySearchResult:
        if not self.available:
            return MemorySearchResult(
                records = [],
                source_available = False,
                provider = self.provider_name,
                error = "XTrace is not configured"
            )

        payload = {
            "query": query,
            "limit": limit,
            "metadata": {
                "user_id": user_id,
                "symbol": symbol
            },
        }

        try:
            async with httpx.AsyncClient(timeout = 10) as client:
                response = await client.post(
                    f"{self.base_url}/memories/search",
                    headers = self._header(),
                    json=payload,
                )

                if response.status_code >= 400:
                    return MemorySearchResult(
                        records = [],
                        source_available = False,
                        provider = self.provider_name,
                        error = f"XTrace search failed with status {response.status_code}"
                    )

                data = response.json()
                raw_records = data.get("records") or data.get("results") or []

                records =  [
                    MemoryRecord(
                        id=str(item.get("id")) if item.get("id") else None,
                        text=str(item.get("text") or item.get("content") or ""),
                        metadata=item.get("metadata") or {},
                        score=item.get("score"),
                        provider=self.provider_name,
                )
                    for item in raw_records[:limit]
                    if item.get("text") or item.get("content")
            ]

                return MemorySearchResult(
                    records=records,
                    source_available=True,
                    provider=self.provider_name,
                    error = None,
                )
            
        except Exception as exc:
            logger.warning(f"XTrace search failed with exception {exc}")
            return MemorySearchResult(
                records = [],
                source_available = False,
                provider = self.provider_name,
                error = f"XTrace search failed with exception {exc}"
            )
        

        
    async def store(
            self,
            text:str,
            *,
            user_id: str | None = None,
            symbol: str | None = None,
            metadata: dict
    )-> MemoryStoreResult:
        
        if not self.available:
            return MemoryStoreResult(
                stored = False,
                provider = self.provider_name,
                error = "XTrace is not configured"
            )

        memory_id = str(uuid4())
        payload = {
            "id": memory_id,
            "text": text,
            "metadata": {
                **(metadata or {}),
                "user_id": user_id,
                "symbol": symbol,
            },
        }

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(
                    f"{self.base_url}/memories",
                    headers=self._header(),
                    json=payload,
                )

                if response.status_code >= 400:
                    return MemoryStoreResult(
                        stored=False,
                        provider=self.provider_name,
                        memory_id=None,
                        error=f"XTrace store failed with status {response.status_code}"
                    )
                
                return MemoryStoreResult(
                    stored=True,
                    provider=self.provider_name,
                    memory_id=memory_id,
                    error=None,
                )
            
        except Exception as exc:
            logger.warning(f"XTrace store failed with exception {exc}")
            return MemoryStoreResult(
                stored=False,
                provider=self.provider_name,
                memory_id=None,
                error=f"XTrace store failed with exception {exc}"
            )


        

        
        

