from loguru import logger

from providers.finance.sec_client import SECClient


class SECTool:
    def __init__(self) -> None:
        self._client = SECClient()

    async def get_filings(
        self,
        symbol: str,
        form_type: str = "10-K",
        hits: int = 3,
    ) -> dict:
        try:
            filings = await self._client.search_filings(
                query=symbol,
                form_type=form_type,
                hits=hits,
            )

            return {
                "filings": filings,
                "total": len(filings),
                "source": "sec",
                "error": None,
            }
        
        except Exception as exc:
            logger.warning(
                f"SEC filings fetch failed for {symbol}: {exc}"
            )

            return {
                "filings": [],
                "total": 0,
                "source": "sec",
                "error": str(exc),
            }

    async def get_filing_document(self, url: str) -> dict:
        try:
            text = await self._client.get_filing_document(url)

            return {
                "text": text[:5000],
                "source": "sec",
                "error": None,
            }

        except Exception as exc:
            logger.warning(
                f"SEC document fetch failed for {url}: {exc}"
            )

            return {
                "text": "",
                "source": "sec",
                "error": str(exc),
            }