from memory.memory_service import MemoryService

class MemoryAgent:
    def __init__(self) -> None:
        self._memory = MemoryService()\
        
    async def run(self , symbol: str , user_id: str | None = None) -> dict:
        try:
            result = await self._memory.get_research_context(
                symbol = symbol,
                user_id = user_id,
                query=f"Research context for {symbol}",
                limit=5,
            )            
            
            if not result.source_available or not result.records:
                return {
                    "memory_summary": "No prior memory context available.",
                    "prior_context": [],
                    "source_available": False,
                    "provider": result.provider,
                    "error": result.error,
                }
            
            prior = [
                {
                    "text" : r.text,
                    "score" : r.score,
                    "metadata" : r.metadata,
                }

                for r in result.records
            ] 
            
            summary = (
                f"Found {len(prior)} prior memory records from {result.provider}."
            )            
            
            return {
                "memory_summary": summary,
                "prior_context": prior,
                "source_available": True,
                "provider": result.provider,
                "error": None,
            }
        
        except Exception as exc:
            return {
                "memory_summary": "Memory unavailable; continuing without prior context.",
                "prior_context": [],
                "source_available": False,
                "provider": "unknown",
                "error": str(exc),
            }