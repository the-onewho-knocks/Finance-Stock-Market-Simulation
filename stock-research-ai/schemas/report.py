from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReportCreate(BaseModel):
    user_id:str
    symbol:str
    content:str
    recommendation:str
    confidence_score:float

class ReportOut(BaseModel):
    id:str
    user_id:str
    symbol:str
    content:str
    recommendation:str
    confidence_score:float
    created_at:datetime

    class Config:
        from_attributes=True