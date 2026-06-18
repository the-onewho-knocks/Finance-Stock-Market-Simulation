from tools.market_tool import MarketTool

class MarketAgent:
    def __init__(self):
        self._tool = MarketTool

    async def run(self , symbol:str) -> dict:
        raw = await self._tool.get_market_data(symbol)

        quote = raw.get("quote" , {})
        profile = raw.get("profile ", {})

        if not quote and not profile:
            return{               
                "market_summary": f"Market data unavailable for {symbol}.",
                "key_metrics": {},
                "error": raw.get("quote_error") or raw.get("profile_error"),
            }
        
        current_price = quote.get("c" , 0)
        percent_change = quote.get("dp" , 0)
        high = quote.get("h" , 0)
        low = quote.get("l" , 0)
        company_name = profile.get("name" , symbol)

        key_metrics = {
            "company_name":company_name,
            "current_price": current_price,
            "percent_change": percent_change,
            "day_high": high,
            "day_low": low,
            "market_cap": profile.get("marketCapitalization"),
            "exchange": profile.get("exchange"),
        }

        summary = (
            f"{company_name} ({symbol}): ${current_price} "
            f"({percent_change:+.2f}% today)"
        )

        return {
            "market_summary": summary,
            "key_metrics": key_metrics,
            "source": "finnhub+polygon",
            "error": None,
        }