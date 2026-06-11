class StockResearchError(Exception):
    """Base exception."""

class ProviderError(StockResearchError):
    """External API provider failed."""
    def __init__(self, provider: str, detail: str):
        self.provider = provider
        super().__init__(f"[{provider}] {detail}")

class SymbolNotFoundError(StockResearchError):
    def __init__(self, symbol: str):
        super().__init__(f"Symbol '{symbol}' not found.")

class LLMError(StockResearchError):
    pass

class RAGError(StockResearchError):
    pass

class DatabaseError(StockResearchError):
    pass

class WatchlistError(StockResearchError):
    pass