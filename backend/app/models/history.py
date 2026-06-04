from datetime import datetime, timezone

from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class GeneratedHistory(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_name: str
    product_description: str
    target_audience: str
    platform_type: str

    caption: str
    short_ad_text: str
    hashtags: list[str] = Field(sa_column=Column(JSON))
    email_subject: str
    cta: str

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
