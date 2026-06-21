from tools.news_tool import NewsTool

class NewsAgent:
    def __init__(self):
        self._tool = NewsTool()

    async def run(self , symbol: str) -> dict:
        raw = await self._tool.get_news(symbol)

        articles = raw.get("articles", [])
        if not articles:
            return {                
                "news_summary": f"No recent news found for {symbol}.",
                "sentiment": "neutral",
                "major_events": [],
                "sources": [],
                "total_articles": 0,
                "error": raw.get("error"),
            }
        
        titles = [a.get("headline" , "") for a in articles[:5]]
        summary = (
            f"Found {len(articles)} recent news articles for {symbol}. "
            f"Top headlines: {'; '.join(titles)}."
        )
         
        sources = [
            {
                "type": "news",
                "title": a.get("headline", ""),
                "url": a.get("url", ""),
                "published_at": str(a.get("datetime") or ""),
            }
            for a in articles[:5]
            if a.get("headline")
        ]

        return {
            "news_summary": summary,
            "sentiment": self._estimate_sentiment(articles),
            "major_events": titles,
            "sources": sources,
            "total_articles": len(articles),
            "error": None,
        }
    
    def _estimate_sentiment(self, articles: list) -> str:
            positive = sum(
                1 for a in articles if "positive" in str(a.get("sentiment", "")).lower()
            )
            negative = sum(
                1 for a in articles if "negative" in str(a.get("sentiment", "")).lower()
            )
            
            if positive > negative:
                return "positive"
            if negative > positive:
                return "negative"
            return "neutral"