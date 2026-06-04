from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    product_name: str = Field(..., min_length=2, max_length=100)
    product_description: str = Field(..., min_length=10, max_length=1000)
    target_audience: str = Field(..., min_length=3, max_length=200)
    platform_type: str = Field(..., pattern="^(Facebook|TikTok|Instagram)$")


class GenerateResponse(BaseModel):
    id: Optional[int] = None
    caption: str
    short_ad_text: str
    hashtags: List[str]
    email_subject: str
    cta: str
    created_at: Optional[datetime] = None


class HistoryItem(BaseModel):
    id: int
    product_name: str
    product_description: str
    target_audience: str
    platform_type: str
    caption: str
    short_ad_text: str
    hashtags: List[str]
    email_subject: str
    cta: str
    created_at: datetime


class HistoryListResponse(BaseModel):
    items: List[HistoryItem]
