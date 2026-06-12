from pydantic import BaseModel
from pydantic import datetime
from typing import Optional

class WatchListAdd(BaseModel):
    user_id:str
    symbol:str
    notes:Optional[str]=None

class WatchListOut(BaseModel):
    id: str
    user_id:str
    symbol:str
    notes:Optional[str]
    created_at:datetime

    class Config:
        from_attributes=True