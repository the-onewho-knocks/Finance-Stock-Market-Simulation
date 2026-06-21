from typing import Any, Optional

from pydantic import BaseModel, Field


class Source(BaseModel):
    type: str
    title: str
    url: Optional[str] = None
    published_at: Optional[str] = None

class ResearchRequest(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol, e.g. AAPL")
    user_id: Optional[str] = None
    deep_analysis: bool = False


class ResearchResponse(BaseModel):
    request_id: str = ""
    symbol: str
    company_name: str = ""
    executive_summary: str = ""
    investment_thesis: str = ""
    recommendation: str = "HOLD"
    confidence_score: float = 0.0
    news_summary: str = ""
    financial_summary: str = ""
    market_summary: str = ""
    sec_summary: str = ""
    memory_summary: str = ""
    key_metrics: dict[str, Any] = Field(default_factory=dict)
    strengths: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    opportunities: list[str] = Field(default_factory=list)
    red_flags: list[str] = Field(default_factory=list)
    sources: list[Source] = Field(default_factory=list)
    agent_outputs: dict[str, Any] = Field(default_factory=dict)
    errors: list[str] = Field(default_factory=list)
    created_at: str = ""