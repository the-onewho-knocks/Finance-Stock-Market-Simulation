from pydantic import BaseModel , Field
from typing import Optional

class ResearchRequest(BaseModel):
    symbol: str = Field(..., description="stock ticker symbol, e.g. AAPL")
    user_id: Optional[str] = None
    deep_analysis: bool = False

class ResearchResponse(BaseModel):
    symbol: str
    company_name: str
    executive_summary:str
    recommendation:str
    confidence_score:float
    news_summary:str
    financial_summary:str
    market_summary:str
    sec_summary:str
    report_id:Optional[str]=None