from typing import Any , Protocol
from pydantic import BaseModel , Field

class MemoryRecord(BaseModel):
    id : str | None = None
    text : str
    metadata: dict[str, Any] = Field(default_factory=dict)
    score: float | None = None
    provider: str = "unknown"


class MemorySearchResult(BaseModel):
    records : list[MemoryRecord] = Field(default_factory=list)
    source_available : bool = False
    provider : str = "none"
    error: str | None = None

class MemoryStoreResult(BaseModel):
    stored: bool = False
    provider: str = "none"
    memory_id : str | None = None
    error: str | None = None

class BaseMemoryProvider(Protocol):
    @property

    async def search(
        self,
        query: str,
        *,
        user_id: str | None = None,
        symboll: str | None = None,
        limit: int = 5,
    ) -> MemorySearchResult:
        ...

    async def store(
        self,
        text: str,
        *,
        user_id: str | None = None,
        symbol: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> MemoryStoreResult:
        ...