from tools.sec_tool import SECTool

class SECAgent:
    def __init__(self):
        self._tool = SECTool()

    async def run(self, symbol: str):
        raw = await self._tool.get_filings(symbol, form_type="10-K", hits=3)
        filings = raw.get("filings", [])
        
        # Consistent return schema for early exit
        if not filings:
            return {
                "sec_summary": f"No SEC filings found for {symbol}",
                "sources": [],
                "risk_factors": [],
                "filing_highlights": "",
                "source": "sec",
                "error": raw.get("error"),
            }
        
        latest = filings[0]
        highlights = latest.get("description") or latest.get("summary") or ""
        highlights_text = str(highlights)[:1500]

        sources = [
            {
                "type": "sec",
                "title": ("; ".join(f["displayNames"]) if isinstance(f.get("displayNames"), list)
                else f.get("displayNames") or f.get("display_name") or f.get("summary") or ""
),
                "url": f.get("url", None),    
            }
            for f in filings[:3]
        ]

        risk_factors = []
        if "risk" in highlights_text.lower():
            risk_factors.append("Risk factor identified in latest filing")

        summary = (            
            f"Found {len(filings)} SEC filings for {symbol}. "
            f"Latest: {highlights_text[:200]}..."
        )

        return {
            "sec_summary": summary,
            "sources": sources,
            "risk_factors": risk_factors,
            "filing_highlights": highlights_text,
            "source": "sec",
            "error": None,
        }